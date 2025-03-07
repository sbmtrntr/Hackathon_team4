'use client';
import React from "react";
import {
  Center, Image, Icon,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Button
} from "@chakra-ui/react";
import { GiHamburgerMenu } from "react-icons/gi";
import { useRouter } from "next/navigation";

const Header: React.FC = () => {
  const router = useRouter();

  const OpenSettings = () => {
    console.log('OpenSettings');
    router.push('/userinfo');
  }
  return (
    <Center>
      {/* ロゴ画像 */}
      <Image
        src='/logo-sample.png'
        h='5vh'
        mt='5'
        cursor={'pointer'}
        onClick={()=>router.push('/')}
      />
      {/* 設定アイコン */}
      <Menu>
        <MenuButton as={Button}>
          <Icon scale="1.5">
            <GiHamburgerMenu />
          </Icon>
        </MenuButton>
        <MenuList>
          <MenuItem>いいねしたユーザ</MenuItem>
          <MenuItem>情報編集</MenuItem>
        </MenuList>
      </Menu>
    </Center>
  );
}

export default Header;
