'use client';

import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
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

const MBTI_TYPES = [
  "INTJ", "INTP", "ENTJ", "ENTP",
  "INFJ", "INFP", "ENFJ", "ENFP",
  "ISTJ", "ISFJ", "ESTJ", "ESFJ",
  "ISTP", "ISFP", "ESTP", "ESFP"
];

const ASSIGNMENT_TYPES = [
  "公共", "金融", "法人", "TC&S","技統本"
];

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: "",
    birthDate: "",
    mbti: "",
    assignment: "",
    email: "",
    password: "",
  });
  const router = useRouter();
  const bgColor = useColorModeValue('white', 'gray.700');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(formData);
    router.push("/dashboard");
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
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
                  <FormLabel>お名前</FormLabel>
                  <Input
                    name="name"
                    placeholder="Data 太郎"
                    value={formData.name}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>生年月日</FormLabel>
                  <Input
                    name="birthDate"
                    type="date"
                    value={formData.birthDate}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>MBTI Type</FormLabel>
                  <Select
                    name="mbti"
                    placeholder="MBTIのタイプは?"
                    value={formData.mbti}
                    onChange={handleChange}
                  >
                    {MBTI_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>配属</FormLabel>
                  <Select
                    name="assignment"
                    placeholder="配属先は？"
                    value={formData.assignment}
                    onChange={handleChange}
                  >
                    {ASSIGNMENT_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>Email</FormLabel>
                  <Input
                    name="email"
                    type="email"
                    placeholder="m@example.com"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </FormControl>

                <FormControl isRequired>
                  <FormLabel>Password</FormLabel>
                  <Input
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                  />
                </FormControl>

                <Button
                  type="submit"
                  colorScheme="blue"
                  size="lg"
                  w="full"
                >
                  Create Account
                </Button>

                <Text textAlign="center" fontSize="sm" color="gray.500">
                  Already have an account?{" "}
                  <Link href="/login" style={{ color: 'blue', textDecoration: 'underline' }}>
                    Sign in
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