'use client';

import {Box,Button,Container,FormControl,FormLabel,
  Heading,Input,Stack,Text,VStack,useColorModeValue,Card,CardBody,CardHeader,
  InputGroup,InputLeftElement
} from '@chakra-ui/react';
import { FaRegUser, FaLock } from "react-icons/fa";
import { CiMail } from "react-icons/ci";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from "@supabase/supabase-js";
import bcrypt from "bcryptjs";

// Supabase クライアントの作成
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
export default function UserInfoEditPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: ""
  });
  const [message, setMessage] = useState("");

  const router = useRouter();
  const bgColor = useColorModeValue('white', 'gray.700');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // パスワードをハッシュ化
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(formData.password, salt);
    // Supabase にユーザー登録
    try{
      const { data, error } = await supabase
        .from('users')
        .select('id, name, slack_id')
        .eq('name', formData.name)
        .eq('email',formData.email)
        //passwordの認証で引っかかる
        //.eq('password',hashedPassword)
        .single();
      if (error) {
        alert(`認証に失敗しました.間違ったメールアドレスやパスワードを入力している可能性があります．`);
        alert(hashedPassword);
        setFormData({ name: '', email: '', password: '' });
        return;
      }
      // 2ページ目へ遷移 (user_idを渡す)
      router.push(`/userinfo/details?userId=${data.id}`);
  }catch(e){
    alert(e);
    // フォームをリセット
    setFormData({ name: '', email: '', password: '' });
  }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <Box minH="100vh" py={12} px={4} bg="gray.50">
      <Container maxW="md">
        <Card bg={bgColor} shadow="xl" borderRadius="xl">
          <CardHeader>
            <VStack spacing={4}>
              <Heading size="md" textAlign="center">プロフィール編集</Heading>
              <Text color="gray.500" textAlign="center">
                編集する内容を入力してください
              </Text>
            </VStack>
          </CardHeader>

          <CardBody>
            <form onSubmit={handleSubmit}>
              <Stack spacing={4}>
                <FormControl isRequired>
                  <FormLabel>ユーザー名</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <FaRegUser color="gray" />
                    </InputLeftElement>
                    <Input
                      name="name"
                      placeholder="Data 太郎"
                      value={formData.name}
                      onChange={handleChange}
                    />
                  </InputGroup>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>メールアドレス</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <CiMail color="gray" />
                    </InputLeftElement>
                    <Input
                      name="email"
                      type="email"
                      placeholder="m@example.com"
                      value={formData.email}
                      onChange={handleChange}
                    />
                  </InputGroup>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>パスワード</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <FaLock color="gray" />
                    </InputLeftElement>
                    <Input
                      name="password"
                      type="password"
                      value={formData.password}
                      onChange={handleChange}
                    />
                  </InputGroup>
                </FormControl>

                <Button type="submit" colorScheme="blue" size="lg" w="full">
                  次へ
                </Button>
              </Stack>
            </form>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
} 