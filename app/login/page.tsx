'use client';

import { useState } from 'react';
import {Box,Button,
  Card,CardBody,CardFooter,CardHeader,
  Center,FormControl,FormLabel,
  Heading,
  Input,InputGroup,InputLeftElement,
  Stack,Text,VStack,
} from '@chakra-ui/react';
import { FaEnvelope, FaLock } from 'react-icons/fa';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import axios from "axios";

export default function CheckEmail() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [userId, setUserId] = useState("");
  const router = useRouter();

  const handleLogin = async (e:React.FormEvent) => {
    e.preventDefault();
    setMessage("");
    setUserId("");
    try {
      const response = await axios.post(`http://localhost:8080/check_email?email=${email}`);
      setMessage(response.data.message);
      //if (response.data.message === "登録を確認") {
        // Slack に登録されている場合、データベースを確認
      const usersResponse = await axios.get("http://localhost:8080/users");
      const users: Array<{ id: string, email: string }> = usersResponse.data.data;
      const user = users.find((user: { email: string }) => user.email === email);
      if (user) {
        setUserId(user.id);
        const queryString = new URLSearchParams({ userId: user.id }).toString();
        router.push(`/dashboard?${queryString}`);
      } else {
        alert("メールアドレスが確認できなかったため，新規登録画面に移行します．");
        router.push("/register");
      }
      
    } catch (error) {
      let errorMessage = "エラーが発生しました";
      if (axios.isAxiosError(error)) {
        errorMessage = error.response?.data?.detail || errorMessage;
      } else {
        errorMessage = "予期しないエラーが発生しました";
      }
      setMessage(errorMessage);
      alert(errorMessage);
    }
  };

  return (
    <Box
      minH="100vw"
      bg="white"
      py={8}
      px={4}
    >
      <Center>
        <Card
          w="full"
          maxW="md"
          borderRadius="lg"
          boxShadow="sm"
          borderWidth="1px"
          borderColor="gray.100"
        >
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
    </Box>
  );
}
