'use client';

import { useState, Suspense } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';
import {
  Box, Button, Container, FormControl, FormLabel,
  Heading, Input, Stack, VStack, Card, CardBody, CardHeader
} from '@chakra-ui/react';
import { Users } from 'lucide-react';
import axios from 'axios';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try{
      const response = await axios.get(`http://localhost:8080/check_email?email=${formData.email}`);
      const slack_id_n = response.data.slack_id;
      const message = response.data.message;

      // パスワードをハッシュ化
      const salt = await bcrypt.genSalt(10);
      const hashedPassword = await bcrypt.hash(formData.password, salt);

      // Supabase にユーザー登録
      const { data, error } = await supabase
        .from('users')
        .insert([{ name: formData.name, 
                  email: formData.email, 
                  slack_id: slack_id_n,
                  password_hash: hashedPassword,
                  created_at: new Date().toISOString()}])
        .select('id')  // 挿入後にuser_idを取得
        .single();
      if (error) {
        alert(`メールアドレス登録に失敗しました.既にメールアドレスを登録している可能性があります．`);
        setFormData({ name: '', email: '', password: '' });
        return;
      }
    // 2ページ目へ遷移 (user_idを渡す)
    router.push(`/register/details?userId=${data.id}`);
    }catch(e){
      let errorMessage = "Slackワークスペースに登録したメールアドレスを入力してください．";
      alert(errorMessage);
      // フォームをリセット
      setFormData({ name: '', email: '', password: '' });
    }
  };

  return (
    <Box minH="100vh" py={12} px={4} bg="gray.50">
      <Container maxW="md">
        <Card shadow="xl" borderRadius="xl">
          <CardHeader>
            <VStack spacing={4}>
              <Box display="flex" alignItems="center">
                <Box as={Users} boxSize="8" color="blue.500" />
                <Heading ml={2} size="lg">アカウント登録</Heading>
              </Box>
              <Heading size="md">新規作成</Heading>
            </VStack>
          </CardHeader>

          <CardBody>
            <Suspense>
              <form onSubmit={handleSubmit}>
                <Stack spacing={4}>
                  <FormControl isRequired>
                    <FormLabel>お名前</FormLabel>
                    <Input name="name" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel>Email</FormLabel>
                    <Input name="email" type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel>Password</FormLabel>
                    <Input name="password" type="password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} />
                  </FormControl>

                  <Button type="submit" colorScheme="blue" size="lg" w="full">次へ</Button>
                </Stack>
              </form>
            </Suspense>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}
