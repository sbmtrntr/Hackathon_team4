"use client";
import React from "react";

import {
  Center, VStack, Box, Heading, Text, List, ListItem, ListIcon, Button, Badge,
  Wrap,
  WrapItem
} from "@chakra-ui/react";

const users = [
  {
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

const LikesPage = () => {
  const handleClick = (userName: string) => {
    alert(`${userName} と Slack で話すボタンが押されました！`);
  };

  const checkMatch = (user: string) => {
    if (user === "ユーザーA" || user === "ユーザーC") {
      return true;
    }
    return false;
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
              <Heading as="h1" size="md" color="gray.800" borderBottom="2px solid" pb={2}>
                いいねしたユーザ
              </Heading>
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
                      <VStack>
                        {checkMatch(user.name) && (
                          <Badge colorScheme="orange">マッチしています</Badge>
                        )}
                        <Text>
                          {user.name}
                        </Text>
                      </VStack>
                      {checkMatch(user.name) && (
                        <>

                          <Button
                            onClick={() => handleClick(user.name)}
                            textColor="white"
                            bg="#235180"
                            size="sm"
                          >
                            Slackで話す
                          </Button>
                        </>
                      )}
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

export default LikesPage;
