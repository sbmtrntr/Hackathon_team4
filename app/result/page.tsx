"use client";
import React, { useState } from "react";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, ListIcon, Button, Badge,
  Icon,
  Wrap,
  WrapItem
} from "@chakra-ui/react";

import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai'

const users = [
  {
    user_id: "1",
    name: "ユーザーA",
    hobbies: "読書, 旅行, 映画鑑賞",
    hometown: "東京都",
    field: "公共",
    role: "SE",
    mbti: "INTJ",
    alma_mater: "東京大学",
    preferences: "hometown"
  },
  {
    user_id: "2",
    name: "ユーザーB",
    hobbies: "料理, 登山, 音楽",
    hometown: "大阪府",
    field: "医療",
    role: "データアナリスト",
    mbti: "ENTP",
    alma_mater: "京都大学",
    preferences: "field"
  },
  {
    user_id: "3",
    name: "ユーザーC",
    hobbies: "ゲーム, プログラミング, 筋トレ",
    hometown: "福岡県",
    field: "IT",
    role: "エンジニア",
    mbti: "INFJ",
    alma_mater: "九州大学",
    preferences: "mbti"
  },
  {
    user_id: "4",
    name: "ユーザーD",
    hobbies: "ランニング, スポーツ観戦, 写真",
    hometown: "北海道",
    field: "教育",
    role: "教師",
    mbti: "ISTP",
    alma_mater: "北海道大学",
    preferences: "alma_mater"
  },
  {
    user_id: "5",
    name: "ユーザーE",
    hobbies: "読書, カフェ巡り, ガーデニング",
    hometown: "愛知県",
    field: "経済",
    role: "コンサルタント",
    mbti: "ENTJ",
    alma_mater: "名古屋大学",
    preferences: "role"
  }
];

export default function MatchingResult() {
  const [likes, setLikes] = useState<{ [key: string]: boolean }>({});
  const toggleLike = (userId: string) => {
    setLikes((prevLikes) => ({
      ...prevLikes,
      [userId]: !prevLikes[userId]
    }));
    // ここでlikeの状態を更新するapiを叩きます
  };


  return (
    <Center mt={10}>
      <VStack spacing={6}>
        <Box
          maxW="lg"
          mx="auto"
          bg="white"
          boxShadow="lg"
          borderRadius="lg"
          p={6}
          textAlign="center"
        >
          <Heading as="h1" size="xl" color="gray.800" borderBottom="2px solid" pb={2}>
            🎉 マッチング結果 🎉
          </Heading>
          <Text fontSize="lg" color="gray.700" mt={4}>
            あなたにぴったりなユーザーを見つけました！
          </Text>
          <List bg="gray.100" borderRadius="lg" p={4} boxShadow="md" mt={4} spacing={3}>
            {users.map((user) => (
              <ListItem
                key={user.name}
                fontSize="xl"
                fontWeight="semibold"
                color="gray.800"
                p={4}
                borderLeft="4px solid"
                borderColor="blue.500"
                display="flex"
                flexDirection="column"
                alignItems="start"
                gap={2}
              >
              <Box display="flex" justifyContent="space-between" width="100%" alignItems="center">
                <Text>{user.name}</Text>

                <Button
                  onClick={() => toggleLike(user.user_id)}
                  textColor="white"
                  bg="#FF9800"
                  size="sm"
                  _hover={{ bg: "#FF9800", transform: "scale(1.05)" }}
                  leftIcon={
                    <Icon
                      as={likes[user.user_id] ? AiFillHeart : AiOutlineHeart}
                      fontSize="16px"
                      color={likes[user.user_id] ? 'red.400' : 'gray.500'}
                    />
                  }
                >
                  {likes[user.user_id] ? "いいね済" : "いいね"}
                </Button>
              </Box>


                <Box fontSize="md" color="gray.600" pl={6} textAlign="left">
                  <Text>🎭 MBTI:{user.mbti}</Text>
                  <Text>🏠 出身地: {user.hometown}</Text>
                  <Text>🏢 志望分野:{user.field}</Text>
                  <Text>💼 志望役割: {user.role}</Text>
                  <Text>🎓 出身大学: {user.alma_mater}</Text>
                  <Text fontWeight="bold" mt={2}>🎨 趣味</Text>
                  <Wrap mt={1}>
                    {user.hobbies.split(", ").map((hobby, index) => (
                      <WrapItem key={index}>
                        <Badge colorScheme="blue" px={2} py={1} borderRadius="md">
                          {hobby}
                        </Badge>
                      </WrapItem>
                    ))}
                  </Wrap>
                </Box>
              </ListItem>
            ))}
          </List>
        </Box>
      </VStack>
    </Center>
  );
}
