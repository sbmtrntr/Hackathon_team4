'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Center,
  FormControl,
  FormLabel,
  Heading,
  Icon,
  Input,
  InputGroup,
  InputLeftElement,
  Text,
  VStack,
} from '@chakra-ui/react';
import { FaCheckCircle, FaEnvelope } from 'react-icons/fa';
import Link from 'next/link';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // ここにパスワードリセット処理を実装
    console.log('Password reset request for:', email);
    setIsSubmitted(true);
  };

  return (
    <Box
      minH="100vh"
      bgGradient="linear(to-b, white.50, pink.100)"
      py={8}
      px={4}
    >
      <Center>
        <Card
          w="full"
          maxW="md"
          borderRadius="lg"
          boxShadow="md"
        >
          <CardHeader pb={0}>
            <VStack spacing={1}>
              <Heading size="lg" textAlign="center">パスワードをお忘れですか？</Heading>
              <Text color="gray.500" textAlign="center">
                登録したメールアドレスを入力してください。パスワードリセットのリンクをお送りします。
              </Text>
            </VStack>
          </CardHeader>

          <CardBody>
            {!isSubmitted ? (
              <form onSubmit={handleSubmit}>
                <VStack spacing={4}>
                  <FormControl isRequired>
                    <FormLabel htmlFor="email">メールアドレス</FormLabel>
                    <InputGroup>
                      <InputLeftElement pointerEvents="none">
                        <FaEnvelope color="gray.300" />
                      </InputLeftElement>
                      <Input
                        id="email"
                        type="email"
                        placeholder="your@email.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </InputGroup>
                  </FormControl>

                  <Button type="submit" w="full" mt={2} colorScheme='blue'>
                    リセットリンクを送信
                  </Button>
                </VStack>
              </form>
            ) : (
              <VStack spacing={4} p={4} textAlign="center">
                <Icon as={FaCheckCircle} w={16} h={16} color="green.500" />
                <Heading as="h3" size="md" color="gray.800">メールを送信しました</Heading>
                <Text color="gray.600">
                  {email} 宛にパスワードリセットのリンクを送信しました。メールをご確認ください。
                </Text>
                <Text color="gray.500" fontSize="sm">
                  メールが届かない場合は、迷惑メールフォルダをご確認いただくか、別のメールアドレスでお試しください。
                </Text>
              </VStack>
            )}
          </CardBody>

          <CardFooter pt={0} justifyContent="center">
            <Link href="/login" passHref>
              <Box as="span" color="brand.500" fontSize="sm" _hover={{ textDecoration: 'underline' }}>
                ログインページに戻る
              </Box>
            </Link>
          </CardFooter>
        </Card>
      </Center>
    </Box>
  );
}