"use client";
import React, { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import axios from "axios";
import {
  Center, VStack, Box, Heading, Text, List, ListItem, Button, Badge, Wrap, WrapItem
} from "@chakra-ui/react";
import { useSearchParams } from "next/navigation";
import router from "next/router";
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
  isMatched: boolean;
};

const LikesPage = () => {
  const [likedUsers, setLikedUsers] = useState<UserAttributes[]>([]);
  //const [userId, setUserId] = useState<string | null>(null);
  const [mySlackId, setMySlackId] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const userId = searchParams.get('userId');
  useEffect(() => {
    const fetchLikedUsers = async () => {
      // 自分の Slack ID を取得
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

      // Likesテーブルから自身がいいねしたtarget_user_idを取得
      const { data: likes, error: likesError } = await supabase
        .from("likes")
        .select("target_user_id")
        .eq("user_id", userId);

      if (likesError) {
        console.error("Likesテーブルの取得エラー:", likesError);
        return;
      }

      if (likes.length === 0) return;

      // いいねしたユーザーのID一覧
      const targetUserIds = likes.map((like) => like.target_user_id);

      // target_user_idをもとにuser_attributesテーブルを検索
      const { data: users, error: usersError } = await supabase
        .from("user_attributes")
        .select("user_id, hobbies, hometown, field, role, mbti, alma_mater")
        .in("user_id", targetUserIds);

      if (usersError) {
        console.error("user_attributesの取得エラー:", usersError);
        return;
      }

      // 自分をいいねしたユーザーを取得（マッチングチェック用）
      const { data: likedMe, error: likedMeError } = await supabase
        .from("likes")
        .select("user_id")
        .eq("target_user_id", userId); // 自分をいいねした人を取得

      if (likedMeError) {
        console.error("マッチング判定のエラー:", likedMeError);
        return;
      }

      // いいねされたユーザーのID一覧
      const likedMeIds = likedMe.map((like) => like.user_id);

      // マッチしているユーザーには isMatched: true を追加
      const enrichedUsers = users.map((user) => ({
        ...user,
        isMatched: likedMeIds.includes(user.user_id),
      }));

      setLikedUsers(enrichedUsers);
    };

    fetchLikedUsers();
  }, []);

  const handleSlackRedirect = async (user: UserAttributes) => {
    if (!mySlackId) {
      console.error("自分の Slack ID が取得できていません");
      return;
    }

    // 相手の Slack ID を取得
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
      if (response.status === 200) {
        window.location.href = response.data.URL; // Slack のリダイレクト URL に移動
      } else {
        console.error("Slack リダイレクトエラー:", response.data);
      }
    } catch (error) {
      console.error("Slack API エラー:", error);
    }
  };

  return (
    <Center mt={10}>
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
                  </Box>
                </ListItem>
              ))
            )}
          </List>
        </Box>
      </VStack>
    </Center>
  );
}

export default LikesPage;

