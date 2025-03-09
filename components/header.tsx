'use client';
import React, { useEffect, useState } from "react";
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
import { usePathname, useSearchParams } from 'next/navigation'; // 追加

const Header: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname(); // 現在のパスを取得
  const searchParams = useSearchParams(); // クエリパラメータを取得
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    const userId = searchParams.get('userId'); // クエリパラメータからuserIdを取得

    // URLに"userId"が含まれているか、または特定のパスかをチェック
    if (userId || pathname === "/likes" || pathname === "/userinfo") {
      setShowMenu(true);
    } else {
      setShowMenu(false);
    }
  }, [pathname, searchParams]);

  const movePage = (path: string) => {
    console.log(`${path}に移動したよ`);
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
        onClick={() => router.push('/')}
      />
      
      {/* メニュー */}
      {showMenu && (
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
