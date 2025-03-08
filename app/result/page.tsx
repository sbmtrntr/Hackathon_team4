"use client";
import React, { useState, useEffect } from "react";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, Button, Badge,
  Icon, Wrap, WrapItem, Textarea
} from "@chakra-ui/react";
import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai';
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// ユーザーの型定義
type User_attributes = {
  user_id: string;
  hobbies: string;
  field: string;
  role: string;
  mbti: string;
  alma_mater: string;
  preferences: string;
  hometown: string;
  name?: string;
};

type User = {
  id: string;
  name: string;
  slack_id: string;
};

type LikeState = {
  [key: string]: { liked: boolean; reason: string };
};

const MatchingResult = () => {
  const [users_attributes, setUsersA] = useState<User_attributes[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [likes, setLikes] = useState<LikeState>({});
  const [currentUserId, setCurrentUserId] = useState<string>("");

  useEffect(() => {
    const fetchData = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const userId = urlParams.get("userId") || "";
      const userIds = urlParams.getAll("user_ids");

      if (userId) {
        setCurrentUserId(userId);
      }

      if (userIds.length > 0) {
        const { data, error } = await supabase
          .from("user_attributes")
          .select("user_id, hometown, hobbies, field, role, mbti, alma_mater, preferences")
          .in("user_id", userIds);

        if (error) {
          console.log("Error fetching user attributes:", error);
          alert(error);
        } else {
          setUsersA(data);
        }

        const { data: usersData, error: usersError } = await supabase
          .from("users")
          .select("id, name, slack_id")
          .in("id", userIds);

        if (usersError) {
          console.log("Error fetching users:", usersError);
          alert(usersError);
        } else {
          setUsers(usersData);
        }
      }
    };

    fetchData();
  }, []);

  const handleLike = (targetUserId: string) => {
    setLikes((prevLikes) => ({
      ...prevLikes,
      [targetUserId]: { liked: !prevLikes[targetUserId]?.liked, reason: "" },
    }));
  };

  const handleReasonChange = (targetUserId: string, reason: string) => {
    setLikes((prevLikes) => ({
      ...prevLikes,
      [targetUserId]: { ...prevLikes[targetUserId], reason },
    }));
  };

  const submitLike = async (targetUserId: string) => {
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get("userId") || "";
    if (!userId || !likes[targetUserId]?.reason) return;

    const { error } = await supabase.from("likes").insert([
      { user_id: userId, target_user_id: targetUserId, reasons: likes[targetUserId].reason },
    ]);

    if (error) {
      console.log("Error saving like:", error);
      //alert(error.message);
      alert("いいねの保存に失敗しました。");
    } else {
      alert("いいねを保存しました！");
    }
  };

  return (
    <Center mt={10}>
      <VStack spacing={6}>
        <Box maxW="lg" bg="white" boxShadow="lg" borderRadius="lg" p={6}>
          <Heading as="h1" size="xl" color="gray.800">🎉 マッチング結果 🎉</Heading>
          <Text fontSize="lg" color="gray.700" mt={4}>
            あなたにぴったりなユーザーを見つけました！
          </Text>
          <List spacing={3}>
            {users_attributes.map((user_attributes) => {
              const user = users.find((u) => u.id === user_attributes.user_id);
              return user ? (
                <ListItem key={user_attributes.user_id} p={4} borderLeft="4px solid blue">
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Button onClick={() => handleLike(user_attributes.user_id)}>
                      <Icon
                        as={likes[user_attributes.user_id]?.liked ? AiFillHeart : AiOutlineHeart}
                        color={likes[user_attributes.user_id]?.liked ? "red.400" : "gray.500"}
                      />
                      {likes[user_attributes.user_id]?.liked ? "いいね済" : "いいね"}
                    </Button>
                  </Box>

                  <Box>
                    <Text>🎭 MBTI: {user_attributes.mbti}</Text>
                    <Text>🏠 出身地: {user_attributes.hometown}</Text>
                    <Text>🏢 志望分野: {user_attributes.field}</Text>
                    <Text>💼 志望役割: {user_attributes.role}</Text>
                    <Text>🎓 出身大学: {user_attributes.alma_mater}</Text>
                    <Wrap mt={1}>
                      {user_attributes.hobbies.split(", ").map((hobby, index) => (
                        <WrapItem key={index}>
                          <Badge colorScheme="blue">{hobby}</Badge>
                        </WrapItem>
                      ))}
                    </Wrap>
                  </Box>

                  {likes[user_attributes.user_id]?.liked && (
                    <Box mt={3}>
                      <Textarea
                        placeholder="いいねの理由を入力"
                        value={likes[user_attributes.user_id]?.reason || ""}
                        onChange={(e) => handleReasonChange(user_attributes.user_id, e.target.value)}
                      />
                      <Button mt={2} onClick={() => submitLike(user_attributes.user_id)}>
                        送信
                      </Button>
                    </Box>
                  )}
                </ListItem>
              ) : null;
            })}
          </List>
        </Box>
      </VStack>
    </Center>
  );
};

export default MatchingResult;
