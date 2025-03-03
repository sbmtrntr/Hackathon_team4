'use client';
import React from "react";
import { Center, Image, IconButton } from "@chakra-ui/react";
import { IoSettingsOutline } from "react-icons/io5";
import { useRouter } from "next/navigation";

const Header: React.FC = () => {
  const router = useRouter();

  const OpenSettings = () => {
    console.log('OpenSettings');
    router.push('/userinfo');
  }
  return (
    <Center>
      <Image src='logo-sample.png' h='5vh' mt='5'/>
      <IconButton
        icon={<IoSettingsOutline/>}
        fontSize={20} mt='5'
        aria-label="ユーザ設定"
        onClick={()=>OpenSettings()}
      />
    </Center>
  );
}

export default Header;
