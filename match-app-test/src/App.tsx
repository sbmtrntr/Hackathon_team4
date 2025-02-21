import { useState, use, Suspense } from 'react';
import axios from 'axios';
import { HeartIcon, SearchIcon, UsersIcon } from './components/Icons';
import { ErrorBoundary } from './components/ErrorBoundary';

interface Profile {
  name: string;
  birthDate: string;
  prefecture: string;
}

interface MatchedProfile {
  name: string;
  birthDate: string;
  prefecture: string;
}

interface SheetsResponse {
  values: string[][];
}

function MatchResults({ url, profile }: { url: string; profile: Profile }) {
  const values = use(fetchProfiles(url));
  
  const profiles: MatchedProfile[] = values.map((row: string[]) => ({
    name: row[0] || '',
    birthDate: row[1] || '',
    prefecture: row[2] || ''
  }));

  const matches = profiles.filter(p => 
    p.prefecture === profile.prefecture && 
    p.name !== profile.name
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {matches.map((match, index) => (
        <div key={index} className="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
          <h3 className="font-medium text-gray-800">{match.name}</h3>
          <p className="text-gray-600 text-sm">出身地: {match.prefecture}</p>
        </div>
      ))}
    </div>
  );
}

async function fetchProfiles(url: string) {
  const response = await axios.get<SheetsResponse>(url);
  return response.data.values || [];
}

function App() {
  const [profile, setProfile] = useState<Profile>({
    name: '',
    birthDate: '',
    prefecture: ''
  });
  const [isSearching, setIsSearching] = useState(false);

  const API_KEY = import.meta.env.REACT_APP_GOOGLE_SHEETS_API_KEY;
  const SHEET_ID = import.meta.env.REACT_APP_GOOGLE_SHEETS_DOC_ID;
  const RANGE = 'Sheet1';
  const SHEETS_API_URL = `https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${RANGE}?key=${API_KEY}`;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSearching(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-rose-50 to-white">
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center mb-8">
          <HeartIcon className="w-12 h-12 text-rose-500 mx-auto mb-2" />
          <h1 className="text-3xl font-semibold text-gray-800 mb-2">内定者マッチングアプリ</h1>
          <p className="text-gray-600">まだ見ぬ友人たちに会いに行こう</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                お名前
              </label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-200"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                生年月日
              </label>
              <input
                type="date"
                value={profile.birthDate}
                onChange={(e) => setProfile({ ...profile, birthDate: e.target.value })}
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-200"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                出身地
              </label>
              <select
                value={profile.prefecture}
                onChange={(e) => setProfile({ ...profile, prefecture: e.target.value })}
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-200"
                required
              >
                <option value="">選択してください</option>
                <option value="北海道">北海道</option>
                <option value="東京都">東京都</option>
                <option value="大阪府">大阪府</option>
                <option value="福岡県">福岡県</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full px-4 py-2 bg-rose-500 text-white rounded-lg hover:bg-rose-600 transition-colors flex items-center justify-center gap-2"
            >
              <SearchIcon className="w-5 h-5" />
              マッチングを探す
            </button>
          </form>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
            <UsersIcon className="w-6 h-6" />
            マッチング結果
          </h2>
          
          {isSearching ? (
            <ErrorBoundary
              fallback={
                <div className="bg-red-50 text-red-600 p-4 rounded-lg">
                  データの取得中にエラーが発生しました。
                </div>
              }
            >
              <Suspense
                fallback={
                  <div className="text-center text-gray-500 py-8">
                    検索中...
                  </div>
                }
              >
                <MatchResults url={SHEETS_API_URL} profile={profile} />
              </Suspense>
            </ErrorBoundary>
          ) : (
            <div className="text-center text-gray-500 py-8">
              まだマッチングが見つかっていません。
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;