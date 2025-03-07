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
type User = {
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

const MatchingResult = () => {
  const [users, setUsers] = useState<User[]>([]);  // usersの型をUser[]に指定
  const [likes, setLikes] = useState<{ [key: string]: boolean }>({});
  
  useEffect(() => {
    const fetchData = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const userIds = urlParams.get("user_ids")?.split(",") || [];
      alert(userIds);
      if (userIds.length > 0) {
        const { data, error } = await supabase
          .from('user_attributes')
          .select('user_id, hometown, hobbies, field, role, mbti, alma_mater, preferences')  // hometownを追加
          .eq('user_id', userIds);
        
        if (error) {
          console.error('Error fetching users:', error);
        } else {
          setUsers(data);  // 型エラーが解消されます
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
            {users.map((user) => (
              <ListItem
                key={user.user_id}  // ユーザーIDをkeyとして使う
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
};

export default MatchingResult;
