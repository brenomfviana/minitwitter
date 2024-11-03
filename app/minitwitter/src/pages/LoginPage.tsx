import { useState, cache } from "react";
import { useNavigate } from "react-router-dom";
import BaseLayout from "../layouts/BaseLayout";
import TextInput from "../components/TextInput";
import PasswordInput from "../components/PasswordInput";
import api from "../api";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("Please fill in all fields");
      return;
    }
    setError("");
    const payload = {
      username: username,
      password: password,
    };
    api
      .post("/auth/login/", payload)
      .then((response) => {
        localStorage.setItem("auth", JSON.stringify(response.data));
        navigate("/");
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleUsername = (username) => {
    setUsername(username);
  };
  const handlePassword = (password) => {
    setPassword(password);
  };

  return (
    <BaseLayout>
      <div className="flex w-full justify-center items-center">
        <div className="flex flex-col gap-5 p-10 items-center max-w-[480px] rounded-xl shadow-xl bg-[#629584]">
          <h1 className="text-3xl font-bold text-[#E2F1E7] ">
            Sign in to Mini Twitter
          </h1>
          <form
            className="flex flex-col gap-4 items-center"
            onSubmit={handleSubmit}
          >
            <div className="flex flex-col gap-2">
              <TextInput label="Username" setValue={handleUsername} />
              <PasswordInput label="Password" setValue={handlePassword} />
            </div>
            <button className="py-1 px-10 bg-[#387478] hover:bg-[#243642] text-[#E2F1E7] rounded-md">
              Log in
            </button>
          </form>
        </div>
      </div>
    </BaseLayout>
  );
};

export default LoginPage;
