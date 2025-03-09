'use client';
import React from "react";
import {
  Center, Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  IconButton
} from "@chakra-ui/react";
import { GiHamburgerMenu } from "react-icons/gi";
import { useRouter } from "next/navigation";

const Header: React.FC = () => {
  const router = useRouter();

  const movePage = (path: string) => {
    console.log('${path}に移動したよ');
    router.push(path);
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
        <MenuButton as={IconButton} aria-label="Options" icon={<GiHamburgerMenu />} variant="outline" mt='5' />
        <MenuList>
          <MenuItem onClick={() => movePage("/likes")}>いいねしたユーザ</MenuItem>
          <MenuItem onClick={() => movePage("/userinfo")}>情報編集</MenuItem>
        </MenuList>
      </Menu>
    </Center>
  );
}

export default Header;
