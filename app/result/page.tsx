"use client";
import { Center, Button, VStack, Box, Heading, Text, List, ListItem, ListIcon } from "@chakra-ui/react";
import React from "react";

const users = ["ユーザーA", "ユーザーB", "ユーザーC", "ユーザーD", "ユーザーE"];

const Result: React.FC = () => {

  const handleClick = (userName) => {
    alert(`${userName} と Slack で話すボタンが押されました！`);
    // 実際にはここで Slack のリンクに飛ばす処理を実装
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
                key={user}
                fontSize="xl"
                fontWeight="semibold"
                color="gray.800"
                p={3}
                borderLeft="4px solid"
                borderColor="blue.500"
                display="flex"
                justifyContent="space-between"
                alignItems="center"
              >
                <span>
                  {user}
                </span>
                <Button
                  onClick={() => handleClick(user)}
                  textColor="white"
                  bg="#235180"
                  size="sm"
                >
                  Slackで話す
                </Button>
              </ListItem>
            ))}
          </List>
        </Box>
      </VStack>
    </Center>
  );
}

export default Result;
