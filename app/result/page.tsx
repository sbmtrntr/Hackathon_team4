"use client";
import React, { useState, useEffect } from "react";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, ListIcon, Button, Badge,
  Icon, Wrap, WrapItem
} from "@chakra-ui/react";
import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai';
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// ユーザーの型を定義
type User_attributes = {
  user_id: string;
  hobbies: string;
  field: string;
  role: string;
  mbti: string;
  alma_mater: string;
  preferences: string;
  hometown: string; // hometownを追加
  name?: string;  // nameはSupabaseから取得していない場合があるのでオプショナルに
};

type User = {
  id: string;
  name: string;
  slack_id: string;
};

const MatchingResult = () => {
  const [users_attributes, setUsersA] = useState<User_attributes[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [likes, setLikes] = useState<{ [key: string]: boolean }>({});
  
  useEffect(() => {
    const fetchData = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const userIds = urlParams.getAll("user_ids");  // user_idsが配列で取得される
      console.log(userIds);  // user_idsの取得確認

      if (userIds.length > 0) {
        // user_idsがカンマ区切りで取得されるので、配列として処理する
        const { data, error } = await supabase
          .from('user_attributes')
          .select('user_id, hometown, hobbies, field, role, mbti, alma_mater, preferences, self_introductions')
          .in('user_id', userIds);  // .in()メソッドで複数のuser_idを指定
        
        if (error) {
          console.log('Error fetching user attributes:', error);
          alert(error);
        } else {
          setUsersA(data);  // データをstateにセット
        }

        // usersテーブルも同様に取得
        const { data: usersData, error: usersError } = await supabase
          .from('users')
          .select('id, name, slack_id')
          .in('id', userIds);  // .in()メソッドで複数のuser_idを指定
        
        if (usersError) {
          console.log('Error fetching users:', usersError);
          alert(usersError);
        } else {
          setUsers(usersData);  // ユーザー情報をstateにセット
        }
      }
    };

    fetchData();
  }, []);

  const toggleLike = (userId: string) => {
    setLikes((prevLikes) => ({
      ...prevLikes,
      [userId]: !prevLikes[userId]
    }));
    // Call an API to save the like state here
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
            {users_attributes.map((user_attributes) => {
              const user = users.find(u => u.id === user_attributes.user_id);  // `user_attributes.user_id` に対応するユーザー情報を取得
              return user ? (
                <ListItem
                  key={user_attributes.user_id}
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
                    <Button
                      onClick={() => toggleLike(user_attributes.user_id)}
                      textColor="white"
                      bg="#FF9800"
                      size="sm"
                      _hover={{ bg: "#FF9800", transform: "scale(1.05)" }}
                      leftIcon={
                        <Icon
                          as={likes[user_attributes.user_id] ? AiFillHeart : AiOutlineHeart}
                          fontSize="16px"
                          color={likes[user_attributes.user_id] ? 'red.400' : 'gray.500'}
                        />
                      }
                    >
                      {likes[user_attributes.user_id] ? "いいね済" : "いいね"}
                    </Button>
                  </Box>

                  <Box fontSize="md" color="gray.600" pl={6} textAlign="left">
                    <Text>🎭 MBTI:{user_attributes.mbti}</Text>
                    <Text>🏠 出身地: {user_attributes.hometown}</Text>
                    <Text>🏢 志望分野:{user_attributes.field}</Text>
                    <Text>💼 志望役割: {user_attributes.role}</Text>
                    <Text>🎓 出身大学: {user_attributes.alma_mater}</Text>
                    <Text fontWeight="bold" mt={2}>🎨 趣味</Text>
                    <Wrap mt={1}>
                      {user_attributes.hobbies.split(", ").map((hobby, index) => (
                        <WrapItem key={index}>
                          <Badge colorScheme="blue" px={2} py={1} borderRadius="md">
                            {hobby}
                          </Badge>
                        </WrapItem>
                      ))}
                    </Wrap>
                  </Box>
                </ListItem>
              ) : null;  // ユーザーが見つからない場合はnullを返す
            })}
          </List>
        </Box>
      </VStack>
    </Center>
  );
};

export default MatchingResult;
