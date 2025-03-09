'use client';

import { useState, Suspense } from 'react';
import { Box, Button, Card, CardBody, CardFooter, CardHeader, Center, FormControl, FormLabel, Heading, Input, InputGroup, InputLeftElement, Stack, Text, VStack } from '@chakra-ui/react';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { createClient } from "@supabase/supabase-js";
import bcrypt from "bcryptjs";

// Supabase クライアントの作成
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function CheckEmail() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      // 🔹 Supabase からユーザー情報を取得
      const { data: users, error } = await supabase
        .from("users")
        .select("id, email, password")
        .eq("email", email)
        .eq("password",password)
        .single(); // 1件だけ取得

      if (error || !users) {
        setMessage("メールアドレスが間違っているか，登録されていません．");
        setEmail("");
        setPassword("");
        return;
      }
      // 🔹 ログイン成功 → ダッシュボードへ遷移
      const queryString = new URLSearchParams({ userId: users.id }).toString();
      router.push(`/likes?${queryString}`);

    } catch (error) {
      console.error("ログインエラー:", error);
      setMessage("エラーが発生しました");
      alert("ログインに失敗しました");
    }
  };

  return (
    <Box minH="100vw" bg="white" py={8} px={4}>
      <Suspense>
      <Center>
        <Card w="full" maxW="md" borderRadius="lg" boxShadow="sm" borderWidth="1px" borderColor="gray.100">
          <CardHeader pb={0}>
            <VStack spacing={1}>
              <Heading size="lg" textAlign="center" color="gray.700">ログイン</Heading>
              <Text color="gray.500" textAlign="center">
                アカウントにログインして、同期とつながりましょう
              </Text>
            </VStack>
          </CardHeader>

          <CardBody>
            <form onSubmit={handleLogin}>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel htmlFor="email">メールアドレス</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <FaEnvelope color="gray.300" />
                    </InputLeftElement>
                    <Input id="email" type="email" placeholder="your@email.com" value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      borderColor="gray.200"
                      _focus={{ borderColor: 'brand.500' }}
                    />
                  </InputGroup>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel htmlFor="password">パスワード</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <FaLock color="gray.300" />
                    </InputLeftElement>
                    <Input
                      id="password"
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      borderColor="gray.200"
                      _focus={{ borderColor: 'brand.500' }}
                    />
                  </InputGroup>
                </FormControl>

                <Button type="submit" w="full" mt={2} bg="brand.500" _hover={{ bg: 'brand.600' }}>
                  ログイン
                </Button>

                {message && <Text color="red.500" fontSize="sm">{message}</Text>}
              </VStack>
            </form>
          </CardBody>

          <CardFooter pt={0} flexDirection="column">
            <Stack spacing={2} align="center">
              <Text fontSize="sm" color="gray.500">
                アカウントをお持ちでない方は{' '}
                <Link href="/register" passHref>
                  <Box as="span" color="brand.500" _hover={{ textDecoration: 'underline' }}>
                    新規登録
                  </Box>
                </Link>
              </Text>
              <Link href="/forgot_password" passHref>
                <Box as="span" fontSize="sm" color="gray.500" _hover={{ textDecoration: 'underline' }}>
                  パスワードをお忘れですか？
                </Box>
              </Link>
            </Stack>
          </CardFooter>
        </Card>
      </Center>
      </Suspense>
    </Box>
  );
}