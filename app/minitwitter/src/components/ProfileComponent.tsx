import { useState, useEffect } from "react";
import ProfileCard from "../components/ProfileCard";
import { jwtDecode } from "jwt-decode";
import api from "../api";

const ProfileComponent = () => {
  const [profile, setProfile] = useState("");

  const auth = JSON.parse(localStorage.getItem("auth"));
  api.defaults.headers["Authorization"] = `Bearer ${auth.access}`;
  useEffect(() => {
    const token = jwtDecode(auth.access);

    if (auth) {
      api
        .get(`/users/${token.user_id}/profile/`)
        .then((response) => {
          setProfile(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  }, []);

  return (
    <div className="flex flex-col items-start p-5">
      <ProfileCard user={profile} />
    </div>
  );
};

export default ProfileComponent;
