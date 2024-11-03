import { useState } from "react";

const TextInput = ({ label, setValue }) => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    setValue(value);
  };

  return (
    <>
      <div className="flex flex-col">
        <label className="text-[#E2F1E7]">{label}:</label>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          required
          className="rounded-sm text-[#243642]"
        />
      </div>
    </>
  );
};

export default TextInput;
