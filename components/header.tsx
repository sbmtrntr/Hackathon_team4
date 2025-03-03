'use client';
import React from "react";
import { Center, Image, Icon } from "@chakra-ui/react";
import { IoSettingsOutline } from "react-icons/io5";

const Header: React.FC = () => {
  return (
    <Center>
      <Image src='logo-sample.png' h='5vh' mt='5'/>
      <Icon as={IoSettingsOutline} fontSize={20} mt='5'/>
    </Center>
  );
}

export default Header;
