import React from "react";
import MenuBar from "@/components/base/menubar";
import MatchEdit from "./components/matchEdit";

const UserInfo: React.FC = () => {
  return (
    <MenuBar>
      <div>
        <h1>User Info</h1>
      </div>
      <MatchEdit />
    </MenuBar>
  );
}

export default UserInfo;
