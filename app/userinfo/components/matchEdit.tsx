"use client";
import React, {useState} from "react";
import InputField  from "@/components/base/inputField";
import { Center, VStack, Button } from "@chakra-ui/react";
import { FaLocationDot } from "react-icons/fa6";
import { MdCategory, MdHomeWork } from "react-icons/md";
import { BsFileEarmarkPerson } from "react-icons/bs";
import { IoSchool } from "react-icons/io5";

const MBTI_TYPES = [
  "INTJ", "INTP", "ENTJ", "ENTP",
  "INFJ", "INFP", "ENFJ", "ENFP",
  "ISTJ", "ISFJ", "ESTJ", "ESFJ",
  "ISTP", "ISFP", "ESTP", "ESFP"
];

const ASSIGNMENT_TYPES = [
  "公共", "金融", "法人", "TC&S","技統本"
];

const MatchEdit: React.FC = () => {
  const [formData, setFormData] = useState({
    hometown: "",
    field: "",
    occupation: "",
    mbti: "",
    university: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async () => {
    console.log("送信データ:", formData);
  };

  return (
    <Center>
      <VStack spacing={5}>
        <InputField icon={FaLocationDot} placeholder="出身地" name="hometown" type="text" value={formData.hometown} onChange={handleChange} required />
        <InputField icon={MdCategory} placeholder="志望分野" name="field" type="text" value={formData.field} onChange={handleChange} required/>
        <InputField icon={MdHomeWork} placeholder="志望職種" name="occupation" type="text" value={formData.occupation} onChange={handleChange} required/>
        <InputField icon={BsFileEarmarkPerson} placeholder="MBTI" name="mbti" type="text" value={formData.mbti} onChange={handleChange} required/>
        <InputField icon={IoSchool} placeholder="出身大学" name="university" type="text" value={formData.university} onChange={handleChange} required/>

        <Button bg="#FF9800" textColor='white' onClick={handleSubmit}>
          登録
        </Button>
      </VStack>
    </Center>
  );
}

export default MatchEdit;
