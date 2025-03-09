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
import { usePathname } from "next/navigation"; // usePathnameを使用

const Header: React.FC = () => {
  const pathname = usePathname(); // 現在のパスを取得

  const movePage = (path: string) => {
    console.log(`${path}に移動したよ`);
    window.location.href = path; // `window.location.href`を使って遷移
  };

  // 404ページの場合はメニューを表示しない
  const is404Page = pathname === '/404';

  // メニューを表示するページかどうかの判定
  const isMenuPage = ['/likes', '/userinfo', '/result'].includes(pathname) && !is404Page;

  return (
    <Center>
      {/* ロゴ画像 */}
      <Image
        src='/logo-sample.png'
        h='5vh'
        mt='5'
        cursor={'pointer'}
        onClick={() => window.location.href = '/'} // クリックでホームへ遷移
      />
      
      {/* 404ページでない場合にメニューを表示 */}
      {isMenuPage && (
        <Menu>
          <MenuButton as={IconButton} aria-label="Options" icon={<GiHamburgerMenu />} variant="outline" mt='5' />
          <MenuList>
            <MenuItem onClick={() => movePage("/likes")}>いいねしたユーザ</MenuItem>
            <MenuItem onClick={() => movePage("/userinfo")}>情報編集</MenuItem>
          </MenuList>
        </Menu>
      )}
    </Center>
  );
}

export default Header;
