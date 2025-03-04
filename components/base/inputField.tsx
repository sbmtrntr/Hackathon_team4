import React from "react";
import { Input, InputGroup, InputLeftElement, Icon, Select } from "@chakra-ui/react";

type InputFieldProps = {
  icon: React.ElementType;
  placeholder: string;
  name: string;
  type: string;
  value?: string;
  options?: string[];
  onChange?: (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
}
const InputField: React.FC<InputFieldProps> = ({icon, placeholder, name, type, value, options, onChange}) => {
  return (
    <InputGroup>
      <InputLeftElement pointerEvents="none">
        <Icon as={icon} color="gray.500" />
      </InputLeftElement>

      {options ? (
        <Select name={name} value={value} placeholder={placeholder} bg="white" borderRadius="md" onChange={onChange}>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </Select>
      ) : (
        <Input
          placeholder={placeholder}
          type={type}
          bg="white"
          borderRadius="md"
          name={name}
          value={value}
          onChange={onChange}
        />

      )}
    </InputGroup>
  );
}

export default InputField;
