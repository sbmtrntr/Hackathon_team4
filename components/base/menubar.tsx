import React from 'react';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

type MenuBarProps = {
  children: React.ReactNode;
}
const MenuBar: React.FC<MenuBarProps>= (childcomponents) => {
  return (
    <Tabs size='md' variant='enclosed'>
      <TabList>
        <Tab>基本情報</Tab>
        <Tab>マッチング情報</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          {childcomponents.children}
        </TabPanel>
        <TabPanel>
          { childcomponents.children }
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}

export default MenuBar;
