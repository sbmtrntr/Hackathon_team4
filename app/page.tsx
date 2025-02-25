'use client';

import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
} from '@chakra-ui/react';
import { ArrowRight, Users } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <Box minH="100vh" bg="gray.50">
      <Container maxW="container.xl" py={16}>
        <VStack spacing={8} textAlign="center">
          <Box display="flex" alignItems="center">
            <Box as={Users} boxSize={12} color="blue.500" />
            <Heading ml={2} size="2xl">内定者マッチング</Heading>
          </Box>
          
          <Text fontSize="xl" color="gray.600" maxW="2xl">
            まだ見ぬ友人たちに会いに行こう．
          </Text>

          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} w="full" maxW="5xl" mt={12}>
            <Card>
              <CardHeader>
                <Heading size="md">Join Today</Heading>
              </CardHeader>
              <CardBody>
                <Text color="gray.600">
                  プロフィールを作成して，同じ趣味や高め合える友人との繋がりを作りましょう(*^^*)
                </Text>
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <Heading size="md">Smart Matching</Heading>
              </CardHeader>
              <CardBody>
                <Text color="gray.600">
                  MBTI等から相性の良い仲間を探すことができるよ．
                  素敵な人に出会えるかも😎
                </Text>
              </CardBody>
            </Card>

            <Card>
              <CardHeader>
                <Heading size="md">Let's communication</Heading>
              </CardHeader>
              <CardBody>
                <Text color="gray.600">
                  Slackと連携し，あなたの会話やきっかけ作りをサポートします( ･´ｰ･｀)どや
                </Text>
              </CardBody>
            </Card>
          </SimpleGrid>

          <Link href="/login">
            <Button
              size="lg"
              colorScheme="blue"
              rightIcon={<ArrowRight size={16} />}
              px={8}
            >
              Get Started
            </Button>
          </Link>
        </VStack>
      </Container>
    </Box>
  );
}