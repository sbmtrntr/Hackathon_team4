'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';
import {
  Box, Button, Container, FormControl, FormLabel, Textarea,
  Heading, Select, Stack, VStack, Card, CardBody, CardHeader, Tag, TagLabel, TagCloseButton, Input
} from '@chakra-ui/react';
import { User } from 'lucide-react';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const MBTI_TYPES = [
  "INTJ", "INTP", "ENTJ", "ENTP",
  "INFJ", "INFP", "ENFJ", "ENFP",
  "ISTJ", "ISFJ", "ESTJ", "ESFJ",
  "ISTP", "ISFP", "ESTP", "ESFP"
];

const FIELDS = ["公共", "金融", "法人", "TC&S", "技統本"];
const ROLES = ["営業", "SE", "コンサル", "スタッフ"];
const HOBBIES = [
  "サッカー", "バスケットボール", "野球", "ランニング", "旅行", "映画鑑賞", "アニメ", "漫画", "ゲーム", "カフェ",
  "読書", "音楽", "カメラ", "キャンプ", "筋トレ", "料理", "プログラミング", "ボードゲーム", "ダンス", "登山", 
  "温泉", "釣り", "DIY", "ガーデニング", "スポーツ観戦", "イラスト", "手芸", "ラーメン", "居酒屋", "ボランティア"
];
const PREFECTURES = [
  "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県",
  "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県",
  "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県",
  "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県",
  "宮崎県", "鹿児島県", "沖縄県"
];

const PREFERENCES = [
  "mbti", "hobbies", "hometown", "field", "role", "alma_mater"
];

type User = {
  user_id: string;
  hobbies: string;
  field: string;
  role: string;
  mbti: string;
  alma_mater: string;
  preferences: string;
  hometown: string; // hometownを追加
  self_introductions: string;
  name?: string;  // nameはSupabaseから取得していない場合があるのでオプショナルに
};

export default function RegisterDetailsPage() {
  const router = useRouter();

  // Wrap useSearchParams() inside Suspense
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchParamsWrapper router={router} />
    </Suspense>
  );
}

function SearchParamsWrapper({ router }: { router: any }) {
  const searchParams = useSearchParams();
  const [users, setUsers] = useState<User[]>([]);
  const userId = searchParams.get('userId');

  useEffect(() => {
    const fetchData = async () => {
      const { data, error } = await supabase
        .from('user_attributes')
        .select('user_id, hometown, hobbies, field, role, mbti, alma_mater, preferences, self_introductions')
        .eq('user_id', userId);

      if (error) {
        console.log('Error fetching users:', error);
        alert("ユーザープロフィールが見つかりませんでした．");
        router.push('/userinfo')
        return;
      } else if (data) {
        setUsers(data);
      }
    };

    fetchData();
  }, [userId]);

  const [formData, setFormData] = useState<{
    mbti: string;
    field: string;
    role: string;
    hobbies: string[];
    hometown: string;
    almaMater: string;
    preferences: string;
    self_introductions: string;
  }>({
    mbti: '',
    field: '',
    role: '',
    hobbies: [],
    hometown: '',
    almaMater: '',
    preferences: '',
    self_introductions: '',
  });

  // usersデータが取得されたらformDataに反映
  useEffect(() => {
    if (users.length > 0) {
      const user = users[0];
      setFormData({
        mbti: user.mbti,
        field: user.field || '',
        role: user.role || '',
        hobbies: user.hobbies ? user.hobbies.split(', ') : [],
        hometown: user.hometown || '',
        almaMater: user.alma_mater || '',
        preferences: user.preferences || '',
        self_introductions: user.self_introductions || '',
      });
    }
  }, 
  [users]);
  const handleHobbyToggle = (hobby: string) => {
    setFormData((prev) => {
      const updatedHobbies = prev.hobbies.includes(hobby)
        ? prev.hobbies.filter((h) => h !== hobby)
        : [...prev.hobbies, hobby];
      return { ...prev, hobbies: updatedHobbies };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!userId) return;
      
    const { error } = await supabase
      .from('user_attributes')
      .update([{ 
        user_id: userId, 
        hobbies: formData.hobbies.join(', '), 
        hometown: formData.hometown, 
        field: formData.field, 
        role: formData.role, 
        mbti: formData.mbti, 
        alma_mater: formData.almaMater, 
        preferences: formData.preferences,
        self_introductions: formData.self_introductions}])
      .eq("user_id",userId);

    if (error) {
      alert("登録に失敗しました。");
      return;
    }

    alert("プロフィールを更新しました！");
    router.push(`/matching?userId=${userId}`);
  };

  return (
    <Box minH="100vh" py={12} px={4} bg="gray.50">
        <Container maxW="md">
          <Card shadow="xl" borderRadius="xl">
            <CardHeader>
              <VStack spacing={4}>
                <Heading size="md">プロフィール詳細</Heading>
              </VStack>
            </CardHeader>

            <CardBody>
                <form onSubmit={handleSubmit}>
                  <Stack spacing={4}>
                    <FormControl isRequired>
                      <FormLabel>MBTI</FormLabel>
                      <Select name="mbti" value={formData.mbti} onChange={(e) => setFormData({ ...formData, mbti: e.target.value })}>
                        {MBTI_TYPES.map((type) => <option key={type} value={type}>{type}</option>)}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>希望分野</FormLabel>
                      <Select name="field" value={formData.field} onChange={(e) => setFormData({ ...formData, field: e.target.value })}>
                        {FIELDS.map((field) => <option key={field} value={field}>{field}</option>)}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>希望職種</FormLabel>
                      <Select name="role" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })}>
                        {ROLES.map((role) => <option key={role} value={role}>{role}</option>)}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>趣味</FormLabel>
                      <Stack direction="row" flexWrap="wrap">
                        {HOBBIES.map((hobby) => (
                          <Tag
                            key={hobby}
                            size="lg"
                            variant={formData.hobbies.includes(hobby) ? "solid" : "outline"}
                            colorScheme="blue"
                            cursor="pointer"
                            onClick={() => handleHobbyToggle(hobby)}
                            m={1}
                          >
                            <TagLabel>{hobby}</TagLabel>
                            {formData.hobbies.includes(hobby) && <TagCloseButton />}
                          </Tag>
                        ))}
                      </Stack>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>出身地</FormLabel>
                      <Select name="hometown" value={formData.hometown} onChange={(e) => setFormData({ ...formData, hometown: e.target.value })}>
                        {PREFECTURES.map((prefecture) => <option key={prefecture} value={prefecture}>{prefecture}</option>)}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>出身校</FormLabel>
                      <Input
                        type="text"
                        name="almaMater"
                        value={formData.almaMater}
                        onChange={(e) => setFormData({ ...formData, almaMater: e.target.value })}
                        placeholder="大学名を入力"
                      />
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>重視する項目</FormLabel>
                      <Select name="preferences" value={formData.preferences} onChange={(e) => setFormData({ ...formData, preferences: e.target.value })}>
                        {PREFERENCES.map((preference) => <option key={preference} value={preference}>{preference}</option>)}
                      </Select>
                    </FormControl>
                    
                    {/* 自己紹介 */}
                    <FormControl isRequired>
                      <FormLabel>自己紹介</FormLabel>
                      <Textarea
                        name="self_introductions"
                        value={formData.self_introductions}
                        onChange={(e) => setFormData({ ...formData, self_introductions: e.target.value })}
                        placeholder="自己紹介文を入力してください"/>
                    </FormControl>
                    <Button type="submit" colorScheme="blue" size="lg" w="full">編集完了</Button>
                  </Stack>
                </form>
            </CardBody>
          </Card>
        </Container>
    </Box>
  )
}
