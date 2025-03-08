"use client";

import { Box, Center, Text, Spinner, VStack } from "@chakra-ui/react";
import axios from "axios";
import { motion } from "framer-motion";
import { useRouter, useSearchParams } from "next/navigation";
import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import { CLOUD_RUN_URL } from "@/utils/config";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const MatchingPage = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const userId = searchParams.get('userId');
  const messages = [
    "相性の良い相手を探しています...",
    "共通の趣味の人を見つけています...",
    "特別なご縁を紡いでいます...",
    "マッチング結果を準備中..."
  ];

  const [currentMessage, setCurrentMessage] = useState(messages[0]);
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      if (index === messages.length - 1) {
        setTimeout(async () => {
          try {
                const response = await axios.get(`${CLOUD_RUN_URL}/matching_result?user_id=${userId}`); 
                const userIds = response.data.matches
                  .map((match: any) => match.user_id)
                  .join('&user_ids=');
                router.push(`/result?user_ids=${userIds}`);
              } catch (error) {
                console.error('Error fetching matching results:', error);
              }
        }, 2000);
        clearInterval(interval);
      } else {
        setIndex((prevIndex) => prevIndex + 1);
        setCurrentMessage(messages[index + 1]);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [index, router]);

  return (
    <Box minH="100vh" bgGradient="linear(to-r, pink.50, blue.200)" display="flex" alignItems="center" justifyContent="center">
      <VStack spacing={6}>
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        >
          <Spinner size="xl" color="blue.500" thickness="5px" speed="0.8s" />
        </motion.div>

        <motion.div
          key={currentMessage}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1 }}
        >
          <Text fontSize="lg" fontWeight="bold" color="blue.700">
            {currentMessage}
          </Text>
        </motion.div>
      </VStack>
    </Box>
  );
};

export default MatchingPage;
