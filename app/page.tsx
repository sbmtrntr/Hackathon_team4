'use client';

import {Box,Button,Container,Flex,
  Heading,Icon,Image,SimpleGrid,
  Stack,Text,VStack,
} from '@chakra-ui/react';
import { FaArrowRight, FaUserFriends, FaBuilding, FaGraduationCap, FaComments } from 'react-icons/fa';
import Link from 'next/link';

  return (
    <Box
      bg="white"
      minH="100vh"
    >
      <Container maxW="container.xl" py={16}>
        <VStack spacing={16} textAlign="center">
          {/* Hero Section */}
          <VStack spacing={8}>
            <Flex
              bg="brand.50"
              p={3}
              rounded="full"
              justifyContent="center"
              alignItems="center"
            >
              <Icon as={FaUserFriends} w={12} h={12} color="brand.500" />
            </Flex>
              
            <Text fontSize={{ base: 'lg', md: 'xl' }} color="gray.600" maxW="2xl">
              2025年卒の同期社会人とつながり、新しい友人や仲間を見つけましょう。
              同じタイミングで社会人になった仲間との交流で、充実したキャリアをスタートさせましょう。
            </Text>

            <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
              <Link href="/login" passHref>
                <Button
                  size="lg"
                  rightIcon={<FaArrowRight />}
                  bg="brand.500"
                  _hover={{ bg: 'brand.600' }}
                >
                  ログイン
                </Button>
              </Link>
              <Link href="/register" passHref>
                <Button
                  size="lg"
                  variant="outline"
                  borderColor="brand.200"
                  color="brand.500"
                  _hover={{ bg: 'brand.50' }}
                >
                  新規登録
                </Button>
              </Link>
            </Stack>
          </VStack>

          {/* Features Section */}
          <Box>
            <Heading as="h2" size="xl" mb={12} color="gray.700">
              What's NICOLINK?
            </Heading>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} w="full">
              <Box bg="white" p={6} rounded="xl" shadow="md" borderWidth="1px" borderColor="gray.100">
                <Icon as={FaUserFriends} w={10} h={10} color="brand.500" mb={4} />
                <Heading as="h3" size="md" mb={2} color="gray.700">同期とのつながり</Heading>
                <Text color="gray.600">2025年卒の同期同士で交流。同じ時期に社会人になった仲間との絆を深めましょう</Text>
              </Box>
              <Box bg="white" p={6} rounded="xl" shadow="md" borderWidth="1px" borderColor="gray.100">
                <Icon as={FaBuilding} w={10} h={10} color="brand.500" mb={4} />
                <Heading as="h3" size="md" mb={2} color="gray.700">相性の良い相手との交流</Heading>
                <Text color="gray.600">まだ話したことのない同期と出会い、視野を広げ、新しい知見を得ることができます</Text>
              </Box>
              <Box bg="white" p={6} rounded="xl" shadow="md" borderWidth="1px" borderColor="gray.100">
                <Icon as={FaGraduationCap} w={10} h={10} color="brand.500" mb={4} />
                <Heading as="h3" size="md" mb={2} color="gray.700">成長のためのコミュニティ</Heading>
                <Text color="gray.600">同じ悩みや目標を持つ仲間と共に成長し、キャリアの第一歩を支え合いましょう</Text>
              </Box>
            </SimpleGrid>
          </Box>

          {/* Testimonial Section */}
          <Box bg="brand.50" p={10} rounded="xl" w="full">
            <VStack spacing={6}>
              <Icon as={FaComments} w={10} h={10} color="brand.500" />
              <Heading as="h2" size="lg" color="gray.700">
                ユーザーの声
              </Heading>
              <Text fontSize="lg" fontStyle="italic" color="gray.600" maxW="3xl">
                  ここに誰かのコメント的なやつをつけると胡散臭さが増していい気がします．
                  例として，じろけんさんのやつ貼っていますが，肖像権を失っている方チーム内で募集しています．
              </Text>
              <Flex align="center">
                <Image
                  src="/images/sample.jpg"
                  alt="User"
                  borderRadius="full"
                  boxSize="50px"
                  mr={3}
                />
                <Box textAlign="left">
                  <Text fontWeight="bold" color="gray.700">廣瀬健二朗</Text>
                  <Text fontSize="sm" color="gray.500">ハッカソンチーム4 / 2025年卒</Text>
                </Box>
              </Flex>
            </VStack>
          </Box>

          {/* CTA Section */}
          <VStack spacing={6} p={10} bg="white" rounded="xl" shadow="md" borderWidth="1px" borderColor="gray.100" w="full">
            <Heading as="h2" size="xl" color="brand.500">
              今すぐ始めましょう
            </Heading>
            <Text fontSize="lg" color="gray.600" maxW="2xl">
              2025年卒の同期との新しいつながりがあなたを待っています。<br></br>
              登録して、キャリアの第一歩を共に歩む仲間を見つけましょう。
            </Text>
            <Link href="/register" passHref>
              <Button
                size="lg"
                bg="brand.500"
                _hover={{ bg: 'brand.600' }}
                px={10}
              >
                無料で登録する
              </Button>
            </Link>
          </VStack>
        </VStack>
      </Container>
    </Box>
  );
}