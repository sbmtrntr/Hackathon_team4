import React from 'react';
import { Tabs, TabList, TabPanels, Tab, TabPanel, Center } from '@chakra-ui/react'

type MenuBarProps = {
  children: [React.ReactNode, React.ReactNode];
}
const MenuBar: React.FC<MenuBarProps> = ({children}) => {
  return (
    <Center>
      <Tabs size='md' mt={5} maxWidth="100vw">
        <TabList>
          <Tab>基本情報</Tab>
          <Tab>マッチング情報</Tab>
        </TabList>
        <TabPanels bg='#CFE7FF'>
          <TabPanel>
            {children[0]}
          </TabPanel>
          <TabPanel>
            {children[1]}
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Center>
  );
}

export default MenuBar;
