import React from "react";
import { Input, InputGroup, InputLeftElement, Icon } from "@chakra-ui/react";

type InputFieldProps = {
  icon: React.ElementType;
  placeholder: string;
  type: string;
}
const InputField: React.FC<InputFieldProps> = ({icon, placeholder, type}) => {
  return (
    <InputGroup>
      <InputLeftElement pointerEvents="none">
        <Icon as={icon} color="gray.500" />
      </InputLeftElement>
      <Input placeholder={placeholder} type={type} bg="white" borderRadius="md" />
    </InputGroup>
  );
}

export default InputField;
