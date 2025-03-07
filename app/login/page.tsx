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
} from '@chakra-ui/react';
import { Users } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();
  const bgColor = useColorModeValue('white', 'gray.700');

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    router.push("/dashboard");
  };

  return (
    <Box minH="100vh" py={12} px={4} bg="gray.50">
      <Container maxW="md">
        <Card bg={bgColor} shadow="xl" borderRadius="xl">
          <CardHeader>
            <VStack spacing={4}>
              <Box display="flex" alignItems="center">
                <Box as={Users} boxSize="8" color="blue.500" />
                <Heading ml={2} size="lg">内定者マッチング</Heading>
              </Box>
              <Heading size="md" textAlign="center">Have a good encounter</Heading>
              <Text color="gray.500" textAlign="center">
                メールアドレスとパスワードを入力してください
              </Text>
            </VStack>
          </CardHeader>
          <CardBody>
            <form onSubmit={handleLogin}>
              <Stack spacing={4}>
                <FormControl isRequired>
                  <FormLabel>メールアドレス</FormLabel>
                  <Input
                    type="メールアドレス"
                    placeholder="m@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </FormControl>
                <FormControl isRequired>
                  <FormLabel>パスワード</FormLabel>
                  <Input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="blue"
                  size="lg"
                  w="full"
                >
                  Sign in
                </Button>

                <Text textAlign="center" fontSize="sm" color="gray.500">
                  アカウント登録していないだって?{" "}
                  <Link href="/register" style={{ color: 'blue', textDecoration: 'underline' }}>
                    Sign up
                  </Link>
                </Text>
              </Stack>
            </form>
          </CardBody>
        </Card>
      </Container>
    </Box>
  );
}
