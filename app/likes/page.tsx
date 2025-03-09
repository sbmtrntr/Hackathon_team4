'use client';
import React, { useState, useEffect, Suspense } from "react";
import { createClient } from "@supabase/supabase-js";
import axios from "axios";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, Button, Badge, Wrap, WrapItem
} from "@chakra-ui/react";
import { useSearchParams } from "next/navigation";
import { CLOUD_RUN_URL } from "@/utils/config";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type UserAttributes = {
  user_id: string;
  hobbies: string;
  hometown: string;
  field: string;
  role: string;
  mbti: string;
  alma_mater: string;
  self_introductions: string;
  isMatched: boolean;
  name?: string; // nameを追加
};

const LikesPage = () => {
  return (
    <Center mt={10}>
      <Suspense fallback={<p>Loading...</p>}>
        <LikesPageContent />
      </Suspense>
    </Center>
  );
};

const LikesPageContent = () => {
  const [likedUsers, setLikedUsers] = useState<UserAttributes[]>([]);
  const [mySlackId, setMySlackId] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const searchParams = useSearchParams();

  useEffect(() => {
    setUserId(searchParams.get("userId"));
  }, [searchParams]);

  useEffect(() => {
    if (!userId) return;

    const fetchLikedUsers = async () => {
      const { data: myUserData, error: myUserError } = await supabase
        .from("users")
        .select("slack_id")
        .eq("id", userId)
        .single();

      if (myUserError) {
        console.error("自分のSlack ID取得エラー:", myUserError);
        return;
      }
      setMySlackId(myUserData.slack_id);

      const { data: likes, error: likesError } = await supabase
        .from("likes")
        .select("target_user_id")
        .eq("user_id", userId);

      if (likesError) {
        console.error("Likesテーブルの取得エラー:", likesError);
        return;
      }

      if (likes.length === 0) return;

      const targetUserIds = likes.map((like) => like.target_user_id);

      const { data: users, error: usersError } = await supabase
        .from("user_attributes")
        .select("user_id, hobbies, hometown, field, role, mbti, alma_mater, self_introductions")
        .in("user_id", targetUserIds);

      if (usersError) {
        console.error("user_attributesの取得エラー:", usersError);
        return;
      }

      const { data: userNames, error: userNamesError } = await supabase
        .from("users")
        .select("id, name")
        .in("id", targetUserIds);

      if (userNamesError) {
        console.error("usersテーブルの取得エラー:", userNamesError);
        return;
      }

      const nameMap = userNames.reduce((acc, user) => {
        acc[user.id] = user.name;
        return acc;
      }, {} as Record<string, string>);

      const { data: likedMe, error: likedMeError } = await supabase
        .from("likes")
        .select("user_id")
        .eq("target_user_id", userId);

      if (likedMeError) {
        console.error("マッチング判定のエラー:", likedMeError);
        return;
      }

      const likedMeIds = likedMe.map((like) => like.user_id);
      const enrichedUsers = users.map((user) => ({
        ...user,
        name: nameMap[user.user_id],
        isMatched: likedMeIds.includes(user.user_id),
      }));

      setLikedUsers(enrichedUsers);
    };

    fetchLikedUsers();
  }, [userId]);

  const handleSlackRedirect = async (user: UserAttributes) => {
    if (!mySlackId) {
      console.error("自分の Slack ID が取得できていません");
      return;
    }

    const { data: targetUserData, error: targetUserError } = await supabase
      .from("users")
      .select("slack_id")
      .eq("id", user.user_id)
      .single();

    if (targetUserError) {
      console.error("相手の Slack ID 取得エラー:", targetUserError);
      return;
    }

    const targetSlackId = targetUserData.slack_id;

    try {
      const response = await axios.get(`${CLOUD_RUN_URL}/connect_dm?slack_id1=${mySlackId}&slack_id2=${targetSlackId}`);
      const response_common = await axios.get(`${CLOUD_RUN_URL}/common_attributes?user_id1=${userId}&user_id2=${user.user_id}`);
      const response_bot = await axios.get(`${CLOUD_RUN_URL}/send-greeting?user1_slack_id=${mySlackId}&user2_slack_id=${targetSlackId}&common_point=出身地`);
      
      if (response.status === 200) {
        window.location.href = response.data.URL;
      } else {
        console.error("Slack リダイレクトエラー:", response.data);
      }
      
      if (response_bot.status == 422) {
        window.location.href = response_bot.data.URL;
      }
    } catch (error) {
      console.error("Slack API エラー:", error);
    }    
  };

  const handleChannelRedirect = async () => {
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
    <VStack spacing={6}>
      <Box maxW="lg" mx="auto" bg="white" boxShadow="lg" borderRadius="lg" p={6} textAlign="center">
        <Heading as="h1" size="md" color="gray.800" borderBottom="2px solid" pb={2}>
          いいねしたユーザ
        </Heading>
        <List bg="gray.100" borderRadius="lg" p={4} boxShadow="md" mt={4} spacing={3}>
          {likedUsers.length === 0 ? (
            <Text color="gray.600">いいねしたユーザーがいません</Text>
          ) : (
            likedUsers.map((user) => (
              <ListItem key={user.user_id} fontSize="xl" fontWeight="semibold" color="gray.800" p={4} borderLeft="4px solid" borderColor="blue.500">
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <VStack align="start">
                    {user.isMatched && <Badge colorScheme="orange">マッチしています</Badge>}
                  </VStack>
                  {user.isMatched && (
                    <Button
                      onClick={() => handleSlackRedirect(user)}
                      textColor="white"
                      bg="#235180"
                      size="sm"
                    >
                      Slackで話す
                    </Button>
                  )}
                </Box>
                <Box fontSize="md" color="gray.600" pl={6} textAlign="left">
                  <Text fontSize="2xl" fontWeight="bold" color="blue.600" borderBottom="2px solid #235180">
                    名前: {user.name}
                  </Text>
                  <Text>🎭 MBTI: {user.mbti}</Text>
                  <Text>🏠 出身地: {user.hometown}</Text>
                  <Text>🏢 志望分野: {user.field}</Text>
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
                  <Text fontWeight="bold" mt={3}>📝 自己紹介</Text>
                  <Text color="gray.700" mt={1}>{user.self_introductions}</Text>
                </Box>
              </ListItem>
            ))
          )}
        </List>
      </Box>
    </VStack>
  );
};

export default LikesPage;
