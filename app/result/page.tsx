"use client";
import { Center, Button, VStack, Box, Heading, Text, List, ListItem, ListIcon } from "@chakra-ui/react";
import React from "react";


const Result: React.FC = () => {

  const handleClick = () => {
    console.log("Slackで話す");
  };
  return (
    <Center mt={10}>
      <VStack>
        <Box
        maxW="lg"
        mx="auto"
        bg="white"
        boxShadow="lg"
        borderRadius="lg"
        p={6}
        mt={10}
        textAlign="center"
        >
        <Heading as="h1" size="xl" color="gray.800" borderBottom="2px solid" pb={2}>
          🎉 マッチング結果 🎉
        </Heading>
        <Text fontSize="lg" color="gray.700" mt={4}>
          あなたにぴったりなユーザを見つけました！
        </Text>
        <List bg="gray.100" borderRadius="lg" p={4} boxShadow="md" mt={4}>
          <ListItem fontSize="xl" fontWeight="semibold" color="gray.800" p={3} borderLeft="4px solid" borderColor="blue.500">
            ユーザーA
          </ListItem>
        </List>
      </Box>
        <Button onClick={handleClick} textColor="white" bg="#235180">
          Slackで話す
        </Button>
      </VStack>
    </Center>
  );
}

export default Result;
