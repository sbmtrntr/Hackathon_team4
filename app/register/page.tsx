'use client';

import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Stack,
  Text,
  VStack,
  useColorModeValue,
  Card,
  CardBody,
  CardHeader,
  InputGroup,
  InputLeftElement
} from '@chakra-ui/react';
import { FaRegUser } from "react-icons/fa";
import { CiMail } from "react-icons/ci";
import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    emailConfirm: ""
  });

  const router = useRouter();
  const bgColor = useColorModeValue('white', 'gray.700');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.email !== formData.emailConfirm) {
      alert("メールアドレスが一致しません");
      return;
    }
    console.log(formData);
    router.push("/dashboard");
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
              <Heading size="md" textAlign="center">アカウント作成</Heading>
              <Text color="gray.500" textAlign="center">
                あなたのプロフィールを教えてください
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
                  <FormLabel>メールアドレス（確認）</FormLabel>
                  <InputGroup>
                    <InputLeftElement pointerEvents="none">
                      <CiMail color="gray" />
                    </InputLeftElement>
                    <Input
                      name="emailConfirm"
                      type="email"
                      placeholder="m@example.com"
                      value={formData.emailConfirm}
                      onChange={handleChange}
                    />
                  </InputGroup>
                </FormControl>

                <Button type="submit" colorScheme="blue" size="lg" w="full">
                  Create Account
                </Button>
              </Stack>
            </form>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}