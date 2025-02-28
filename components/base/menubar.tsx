import React from 'react';
import { Tabs, TabList, TabPanels, Tab, TabPanel, Center } from '@chakra-ui/react'

type MenuBarProps = {
  children: React.ReactNode;
}
const MenuBar: React.FC<MenuBarProps>= (childcomponents) => {
  return (
    <Center>
      <Tabs size='md' colorScheme='#CFE7FF' mt={5} maxWidth="480px">
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
    </Center>
  );
}

export default MenuBar;
