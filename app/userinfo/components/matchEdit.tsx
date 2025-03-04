"use client";
import React from "react";
import InputField  from "@/components/base/inputField";
import { Center, VStack } from "@chakra-ui/react";
import { FaLocationDot } from "react-icons/fa6";
import { MdCategory, MdHomeWork } from "react-icons/md";
import { BsFileEarmarkPerson } from "react-icons/bs";
import { IoSchool } from "react-icons/io5";


const MatchEdit: React.FC = () => {
  return (
    <Center>
      <VStack spacing={5}>
        <InputField icon={FaLocationDot} placeholder="出身地" type="text" />
        <InputField icon={MdCategory} placeholder="志望分野" type="text" />
        <InputField icon={MdHomeWork} placeholder="志望職種" type="text" />
        <InputField icon={BsFileEarmarkPerson} placeholder="MBTI" type="text" />
        <InputField icon={IoSchool} placeholder="出身大学" type="text" />
      </VStack>
    </Center>
  );
}

export default MatchEdit;
