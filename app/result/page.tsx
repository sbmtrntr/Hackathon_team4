"use client";
import React, { useState, useEffect } from "react";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, Button, Badge,
  Icon, Wrap, WrapItem, Textarea,
  Spacer
} from "@chakra-ui/react";
import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai';
import { createClient } from "@supabase/supabase-js";
import { CLOUD_RUN_URL } from "@/utils/config";
import axios from "axios";

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
  self_introductions: string;
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
          .select("user_id, hometown, hobbies, field, role, mbti, alma_mater, preferences, self_introductions")
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

  const handleChannelRedirect = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const userId = urlParams.get("userId") || "";
      if (!userId) {
        console.error("userIdが取得できていません");
        return;
      }
  
      try {
        const { data: data, error: error } = await supabase
        .from("users")
        .select("cluster")
        .eq("id", userId)
        .single();
  
        const response = await axios.get(`${CLOUD_RUN_URL}/invite?user_id=${userId}`);
        const response_join = await axios.get(`${CLOUD_RUN_URL}/join_slack_bot?id=${data?.cluster}&common_point=出身地`);
        if (response.status === 200) {
          window.location.href = response.data.URL;
        } else {
          console.error("チャンネルリダイレクトエラー:", response.data);
        }
      } catch (error) {
        console.error("APIエラー:", error);
      }
    };

  return (
    <Center mt={10}>
      <VStack spacing={6}>
        <Box maxW="lg" bg="white" boxShadow="lg" borderRadius="lg" p={6}>
        <Heading as="h1" size="xl" color="gray.800" textAlign="center">🎉 マッチング結果 🎉</Heading>
          <Text fontSize="lg" color="gray.700" textAlign="center">
            あなたにぴったりなユーザーを見つけました！
          </Text>
          <Button 
                  onClick={handleChannelRedirect} 
                  textColor="white"
                  bg="#235180" 
                  size="sm" 
                  alignSelf="flex-start"
                >
                  あなたにオススメのユーザーが集まるチャンネルを覗く👀
                </Button>
          <List spacing={3}>
            {users_attributes.map((user_attributes) => {
              const user = users.find((u) => u.id === user_attributes.user_id);
              return user ? (
                <ListItem key={user_attributes.user_id} p={4} borderLeft="4px solid blue">
                  <Box display="flex" alignItems="center" width="100%">
                    {/* 名前といいねボタンを横並びにする */}
                      <Text fontSize="2xl" fontWeight="bold" color="blue.600" borderBottom="2px solid #235180">
                        名前: {user.name}
                      </Text>
                      <Spacer />
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
                    <Text fontWeight="bold" mt={3}>📝 自己紹介</Text>
                    <Text color="gray.700" mt={1}>{user_attributes.self_introductions}</Text>
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
