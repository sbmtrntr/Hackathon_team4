'use client';

import { useState } from 'react';
import {Box,Button,Card,CardBody,Center,Container,Flex,Heading,SimpleGrid,Text,
  useColorModeValue,VStack,Tag,TagLabel,TagCloseButton,Wrap,WrapItem,Select,
  FormControl,FormLabel,Input,Checkbox,CheckboxGroup,Stack,Tabs,TabList,
  TabPanels,Tab,TabPanel,Divider,
} from '@chakra-ui/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { FaMapMarkerAlt, FaGraduationCap, FaBriefcase, 
  FaUserAlt, FaUniversity,FaHeart
} from 'react-icons/fa';
import axios from "axios";

// 選択可能な項目の定義
const matchingCriteria = [
  { id: 'hobbies', name: '趣味', icon: FaHeart, description: '同じ趣味を持つ人とマッチング' },
  { id: 'hometown', name: '出身地', icon: FaMapMarkerAlt, description: '同じ地域の人とマッチング' },
  { id: 'field', name: '希望分野', icon: FaGraduationCap, description: '同じ分野に興味がある人とマッチング' },
  { id: 'role', name: '希望職種', icon: FaBriefcase, description: '同じキャリアを目指す人とマッチング' },
  { id: 'mbti', name: 'MBTI', icon: FaUserAlt, description: '相性の良い性格の人とマッチング' },
  { id: 'alma_mater', name: '出身校', icon: FaUniversity, description: '同じ大学出身の人とマッチング' },
];

// 趣味の選択肢
const hobbiesOptions = [
  "サッカー", "バスケットボール", "野球", "ランニング", "旅行", "映画鑑賞", 
  "アニメ", "漫画", "ゲーム", "カフェ", "読書", "音楽", "カメラ", "キャンプ", 
  "筋トレ", "料理", "プログラミング", "ボードゲーム", "ダンス", "登山", 
  "温泉", "釣り", "DIY", "ガーデニング", "スポーツ観戦", "イラスト", 
  "手芸", "ラーメン", "居酒屋", "ボランティア"
];

// 都道府県リスト
const prefectures = [
  "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
  "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
  "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
  "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
  "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
  "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
  "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
];

// 希望分野の選択肢
const fieldOptions = ['公共', '法人', '金融', 'TC&S', '技統本'];

// 希望職種の選択肢
const roleOptions = ['SE', '営業', 'コンサル', 'スタッフ'];

// MBTIの選択肢
const mbtiOptions = [
  'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
  'ISTP', 'ISFP', 'INFP', 'INTP',
  'ESTP', 'ESFP', 'ENFP', 'ENTP',
  'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
];

export default function MatchingPage() {
  const [selectedCriteria, setSelectedCriteria] = useState<string[]>([]);
  const [selectedHobbies, setSelectedHobbies] = useState<string[]>([]);
  const [hometown, setHometown] = useState<string>('');
  const [field, setField] = useState<string>('');
  const [role, setRole] = useState<string>('');
  const [mbti, setMbti] = useState<string>('');
  const [almaMater, setAlmaMater] = useState<string>('');
  const [preferences, setPreferences] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState(0);
  
  const router = useRouter();
  const cardBg = useColorModeValue('white', 'gray.700');
  const selectedBg = useColorModeValue('brand.50', 'brand.900');
  const selectedBorder = useColorModeValue('brand.500', 'brand.200');
  const tagColorScheme = 'brand';
  const params = useSearchParams();
  // データをlogin から受け渡し
  const [userdata, setUserData] = useState(params.getAll(""));
  // 項目の選択/選択解除を処理する関数
  const toggleCriterion = (criterionId: string) => {
    setSelectedCriteria(prev => 
      prev.includes(criterionId)
        ? prev.filter(id => id !== criterionId)
        : [...prev, criterionId]
    );
    
    // 項目が選択解除された場合、その項目を重視する項目からも削除
    if (preferences.includes(criterionId) && !selectedCriteria.includes(criterionId)) {
      setPreferences(prev => prev.filter(p => p !== criterionId));
    }
  };

  // 趣味の選択/選択解除を処理する関数
  const toggleHobby = (hobby: string) => {
    if (selectedHobbies.includes(hobby)) {
      setSelectedHobbies(prev => prev.filter(h => h !== hobby));
    } else if (selectedHobbies.length < 3) {
      setSelectedHobbies(prev => [...prev, hobby]);
    }
  };

  // 重視する項目の選択/選択解除を処理する関数
  const togglePreference = (preference: string) => {
    setPreferences(prev => 
      prev.includes(preference)
        ? prev.filter(p => p !== preference)
        : [...prev, preference]
    );
  };

  // マッチング結果画面に遷移する関数
  const handleFindMatches = async (e: React.FormEvent) => {
    // 選択された条件をクエリパラメータとして渡す
    const queryParams = new URLSearchParams();
    
    // 選択された条件を追加
    selectedCriteria.forEach(criterion => {
      queryParams.append('criteria', criterion);
    });
    
    // 各属性の値を追加
    if (selectedHobbies.length > 0) {
      selectedHobbies.forEach(hobby => {
        queryParams.append('hobbies', hobby);
      });
    }
    
    if (hometown) queryParams.append('hometown', hometown);
    if (field) queryParams.append('field', field);
    if (role) queryParams.append('role', role);
    if (mbti) queryParams.append('mbti', mbti);
    if (almaMater) queryParams.append('alma_mater', almaMater);
    
    // 重視する項目を追加
    preferences.forEach(pref => {
      queryParams.append('preferences', pref);
    });
    
    const response = axios.get(`http://localhost:8080/matching_result?user_id=61ecfa1e-6208-4093-ab93-9318f137b0ad`); 
    router.push(`/matching/results?${queryParams.toString()}`);
  };

  // 次のタブに進む
  const nextTab = () => {
    if (activeTab < 1) {
      setActiveTab(activeTab + 1);
    }
  };

  // 前のタブに戻る
  const prevTab = () => {
    if (activeTab > 0) {
      setActiveTab(activeTab - 1);
    }
  };

  // 入力が完了しているかチェック
  const isProfileComplete = () => {
    let isComplete = true;
    
    if (selectedCriteria.includes('hobbies') && selectedHobbies.length === 0) {
      isComplete = false;
    }
    
    if (selectedCriteria.includes('hometown') && !hometown) {
      isComplete = false;
    }
    
    if (selectedCriteria.includes('field') && !field) {
      isComplete = false;
    }
    
    if (selectedCriteria.includes('role') && !role) {
      isComplete = false;
    }
    
    if (selectedCriteria.includes('mbti') && !mbti) {
      isComplete = false;
    }
    
    if (selectedCriteria.includes('alma_mater') && !almaMater) {
      isComplete = false;
    }
    
    return isComplete;
  };

  return (
    <Box
      minH="100vh"
      bg="white"
      py={8}
      px={4}
    >
      <Container maxW="container.lg">
        <VStack spacing={8} align="stretch">
          <Box textAlign="center">
            <Heading
              as="h1"
              size="xl"
              mb={2}
              color="brand.500"
            >
              マッチング条件を選択
            </Heading>
            <Text color="gray.600" fontSize="lg">
              あなたの情報と重視する項目を選んでください。より精度の高いマッチングが可能です。
            </Text>
          </Box>

          <Tabs index={activeTab} onChange={setActiveTab} variant="enclosed" colorScheme="brand">
            <TabList>
              <Tab>重視する項目の選択</Tab>
              <Tab>プロフィール情報の入力</Tab>
            </TabList>

            <TabPanels>
              {/* タブ1: 重視する項目の選択 */}
              <TabPanel>
                <VStack spacing={6} align="stretch">
                  <Text fontSize="lg" fontWeight="medium" color="gray.700">
                    マッチングに使用する項目と重視する項目を選択してください
                  </Text>
                  
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                    {matchingCriteria.map((criterion) => (
                      <Card
                        key={criterion.id}
                        bg={selectedCriteria.includes(criterion.id) ? selectedBg : cardBg}
                        border="2px solid"
                        borderColor={selectedCriteria.includes(criterion.id) ? selectedBorder : 'gray.100'}
                        borderRadius="lg"
                        boxShadow="sm"
                        cursor="pointer"
                        transition="all 0.3s"
                        _hover={{ transform: 'translateY(-5px)', boxShadow: 'md' }}
                        onClick={() => toggleCriterion(criterion.id)}
                      >
                        <CardBody>
                          <VStack spacing={4} align="center" p={2}>
                            <Center
                              bg={selectedCriteria.includes(criterion.id) ? 'brand.100' : 'gray.100'}
                              color={selectedCriteria.includes(criterion.id) ? 'brand.500' : 'gray.500'}
                              w={16}
                              h={16}
                              borderRadius="full"
                            >
                              <Box as={criterion.icon} size="24px" />
                            </Center>
                            <Heading size="md" textAlign="center" color="gray.700">{criterion.name}</Heading>
                            <Text color="gray.600" fontSize="sm" textAlign="center">
                              {criterion.description}
                            </Text>
                            
                            {selectedCriteria.includes(criterion.id) && (
                              <Checkbox 
                                isChecked={preferences.includes(criterion.id)}
                                onChange={() => togglePreference(criterion.id)}
                                colorScheme="brand"
                                size="md"
                                onClick={(e) => e.stopPropagation()}
                              >
                                重視する
                              </Checkbox>
                            )}
                          </VStack>
                        </CardBody>
                      </Card>
                    ))}
                  </SimpleGrid>

                  <Box mt={4}>
                    <Divider mb={4} />
                    <Flex justifyContent="space-between" alignItems="center">
                      <Text color="gray.600">
                        {selectedCriteria.length === 0 ? (
                          "少なくとも1つの項目を選択してください"
                        ) : (
                          `選択中: ${selectedCriteria.length}項目`
                        )}
                      </Text>
                      <Button
                        onClick={nextTab}
                        bg="brand.500"
                        _hover={{ bg: 'brand.600' }}
                        color="white"
                        isDisabled={selectedCriteria.length === 0}
                      >
                        次へ
                      </Button>
                    </Flex>
                  </Box>
                </VStack>
              </TabPanel>

              {/* タブ2: プロフィール情報の入力 */}
              <TabPanel>
                <VStack spacing={6} align="stretch">
                  <Text fontSize="lg" fontWeight="medium" color="gray.700">
                    あなたのプロフィール情報を入力してください
                  </Text>

                  {selectedCriteria.includes('hobbies') && (
                    <Box>
                      <FormLabel fontWeight="medium">趣味（最大3つまで選択可能）</FormLabel>
                      <Text fontSize="sm" color="gray.500" mb={3}>
                        {selectedHobbies.length}/3 選択中
                      </Text>
                      <Wrap spacing={2}>
                        {hobbiesOptions.map((hobby) => (
                          <WrapItem key={hobby}>
                            <Tag
                              size="lg"
                              borderRadius="full"
                              variant={selectedHobbies.includes(hobby) ? "solid" : "outline"}
                              colorScheme={tagColorScheme}
                              cursor="pointer"
                              onClick={() => toggleHobby(hobby)}
                              opacity={selectedHobbies.length >= 3 && !selectedHobbies.includes(hobby) ? 0.5 : 1}
                            >
                              <TagLabel>{hobby}</TagLabel>
                              {selectedHobbies.includes(hobby) && (
                                <TagCloseButton onClick={(e) => {
                                  e.stopPropagation();
                                  setSelectedHobbies(prev => prev.filter(h => h !== hobby));
                                }} />
                              )}
                            </Tag>
                          </WrapItem>
                        ))}
                      </Wrap>
                    </Box>
                  )}

                  {selectedCriteria.includes('hometown') && (
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">出身地</FormLabel>
                      <Select 
                        placeholder="都道府県を選択" 
                        value={hometown} 
                        onChange={(e) => setHometown(e.target.value)}
                      >
                        {prefectures.map((pref) => (
                          <option key={pref} value={pref}>{pref}</option>
                        ))}
                      </Select>
                    </FormControl>
                  )}

                  {selectedCriteria.includes('field') && (
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">希望分野</FormLabel>
                      <Select 
                        placeholder="希望分野を選択" 
                        value={field} 
                        onChange={(e) => setField(e.target.value)}
                      >
                        {fieldOptions.map((option) => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </Select>
                    </FormControl>
                  )}

                  {selectedCriteria.includes('role') && (
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">希望職種</FormLabel>
                      <Select 
                        placeholder="希望職種を選択" 
                        value={role} 
                        onChange={(e) => setRole(e.target.value)}
                      >
                        {roleOptions.map((option) => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </Select>
                    </FormControl>
                  )}

                  {selectedCriteria.includes('mbti') && (
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">MBTI</FormLabel>
                      <Select 
                        placeholder="MBTIを選択" 
                        value={mbti} 
                        onChange={(e) => setMbti(e.target.value)}
                      >
                        {mbtiOptions.map((option) => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </Select>
                    </FormControl>
                  )}

                  {selectedCriteria.includes('alma_mater') && (
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium">出身校</FormLabel>
                      <Input 
                        placeholder="大学名を入力" 
                        value={almaMater} 
                        onChange={(e) => setAlmaMater(e.target.value)}
                      />
                    </FormControl>
                  )}

                  <Box mt={4}>
                    <Divider mb={4} />
                    <Flex justifyContent="space-between">
                      <Button
                        onClick={prevTab}
                        variant="outline"
                        colorScheme="brand"
                      >
                        戻る
                      </Button>
                      <Button
                        size="lg"
                        bg="brand.500"
                        _hover={{ bg: 'brand.600' }}
                        px={10}
                        fontSize="lg"
                        isDisabled={!isProfileComplete()}
                        onClick={handleFindMatches}
                        transition="all 0.3s"
                      >
                        マッチングを開始する
                      </Button>
                    </Flex>
                  </Box>
                </VStack>
              </TabPanel>
            </TabPanels>
          </Tabs>
        </VStack>
      </Container>
    </Box>
  );
}