'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';
import {
  Box, Container, Card, CardHeader, CardBody,
  VStack, Heading, Stack, FormControl, FormLabel,
  Select, Input, Textarea, Button, Tag, TagLabel,
  TagCloseButton, Grid, GridItem, Icon, Tooltip
} from "@chakra-ui/react";
import { FaUser, FaBriefcase, FaMapMarkerAlt, FaUniversity, FaHeart, FaPen } from "react-icons/fa";
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
  const userId = searchParams.get('userId');

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
    self_introductions: ''
  });
  //一旦，コメントアウト
  useEffect(() => {
    if (!userId) {
      alert("ユーザーIDが見つかりません。");
      router.push('/register');
    }
  }, [userId, router]);
  useEffect(() => {
    setFormData((prev) => ({
      ...prev,
      mbti: MBTI_TYPES[0],
      field: FIELDS[0],
      role: ROLES[0],  // 希望職種の初期値を追加
      hometown: PREFECTURES[0],
      preferences: PREFERENCES[0],
    }));
  }, []);

  const handleHobbyToggle = (hobby:any) => {
    setFormData((prev) => ({
      ...prev,
      hobbies: prev.hobbies.includes(hobby)
        ? prev.hobbies.filter((h) => h !== hobby)
        : prev.hobbies.length < 3
          ? [...prev.hobbies, hobby]
          : prev.hobbies
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!userId) return;

    const { error } = await supabase
      .from('user_attributes')
      .insert([{ 
        user_id: userId, 
        hobbies: formData.hobbies.join(', '), 
        hometown: formData.hometown, 
        field: formData.field, 
        role: formData.role, 
        mbti: formData.mbti, 
        alma_mater: formData.almaMater, 
        preferences: formData.preferences,
        self_introductions: formData.self_introductions
      }]);

    if (error) {
      alert(formData.preferences);
      alert("登録に失敗しました。");
      return;
    }

    alert("プロフィールが完成しました！");
    router.push(`/matching?userId=${userId}`);
  };

  return (
    <Box minH="100vh" py={12} px={4} bgGradient="linear(to-r, blue.50, pink.50)">
      <Container maxW="lg">
        <Card shadow="2xl" borderRadius="2xl" bg="white">
          <CardHeader>
            <VStack spacing={4}>
              <Heading size="lg" color="blue.500">プロフィール詳細</Heading>
            </VStack>
          </CardHeader>

          <CardBody>
            <form onSubmit={handleSubmit}>
              <Stack spacing={5}>
                {/* MBTI */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaUser} mr={2} /> MBTI</FormLabel>
                  <Select
                    name="mbti"
                    value={formData.mbti}
                    onChange={(e) => setFormData({ ...formData, mbti: e.target.value })}
                  >
                    {MBTI_TYPES.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </Select>
                </FormControl>

                {/* 希望分野 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaBriefcase} mr={2} /> 希望分野</FormLabel>
                  <Select
                    name="field"
                    value={formData.field}
                    onChange={(e) => setFormData({ ...formData, field: e.target.value })}
                  >
                    {FIELDS.map((field) => (
                      <option key={field} value={field}>{field}</option>
                    ))}
                  </Select>
                </FormControl>

                {/* 希望職種 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaBriefcase} mr={2} /> 希望職種</FormLabel>
                  <Select
                    name="role"
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    {ROLES.map((role) => (
                      <option key={role} value={role}>{role}</option>
                    ))}
                  </Select>
                </FormControl>

                {/* 趣味 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaHeart} mr={2} /> 趣味</FormLabel>
                  <Grid templateColumns="repeat(3, 1fr)" gap={2}>
                    {HOBBIES.map((hobby) => (
                      <GridItem key={hobby}>
                        <Tag
                          size="lg"
                          variant={formData.hobbies.includes(hobby) ? "solid" : "outline"}
                          colorScheme="blue"
                          cursor="pointer"
                          onClick={() => handleHobbyToggle(hobby)}
                        >
                          <TagLabel>{hobby}</TagLabel>
                          {formData.hobbies.includes(hobby) && <TagCloseButton />}
                        </Tag>
                      </GridItem>
                    ))}
                  </Grid>
                </FormControl>

                {/* 出身地 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaMapMarkerAlt} mr={2} /> 出身地</FormLabel>
                  <Select
                    name="hometown"
                    value={formData.hometown}
                    onChange={(e) => setFormData({ ...formData, hometown: e.target.value })}
                  >
                    {PREFECTURES.map((prefecture) => (
                      <option key={prefecture} value={prefecture}>{prefecture}</option>
                    ))}
                  </Select>
                </FormControl>

                {/* 出身校 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaUniversity} mr={2} /> 出身校</FormLabel>
                  <Input
                    type="text"
                    name="almaMater"
                    value={formData.almaMater}
                    onChange={(e) => setFormData({ ...formData, almaMater: e.target.value })}
                    placeholder="大学名を入力"
                  />
                </FormControl>

                {/* 重視する項目 */}
                <FormControl isRequired>
                  <FormLabel><Icon as={FaPen} mr={2} /> 重視する項目</FormLabel>
                  <Select
                    name="preferences"
                    value={formData.preferences}
                    onChange={(e) => setFormData({ ...formData, preferences: e.target.value })}
                  >
                    {PREFERENCES.map((preference) => (
                      <option key={preference} value={preference}>{preference}</option>
                    ))}
                  </Select>
                </FormControl>

                {/* 自己紹介 */}
                <FormControl isRequired>
                  <FormLabel>自己紹介</FormLabel>
                  <Textarea
                    name="self_introductions"
                    value={formData.self_introductions}
                    onChange={(e) => setFormData({ ...formData, self_introductions: e.target.value })}
                    placeholder="自己紹介文を入力してください"
                  />
                </FormControl>

                {/* 登録完了ボタン */}
                <Button
                  type="submit"
                  colorScheme="blue"
                  size="lg"
                  w="full"
                  _hover={{ bg: "blue.600" }}
                >
                  登録完了
                </Button>
              </Stack>
            </form>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}
