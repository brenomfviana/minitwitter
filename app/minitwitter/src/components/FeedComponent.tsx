import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PostCard from "../components/PostCard";
import api from "../api";

const FeedComponent = () => {
  const [feed, setFeed] = useState("");

  const navigate = useNavigate();

  const auth = JSON.parse(localStorage.getItem("auth"));
  api.defaults.headers["Authorization"] = `Bearer ${auth.access}`;
  useEffect(() => {
    if (auth) {
      api
        .get("/feed/")
        .then((response) => {
          setFeed(response.data);
        })
        .catch((error) => {
          console.error(error);
          navigate("/login");
        });
    }
  }, []);

  return (
    <div className="flex flex-col justify-center items-center max-w-[650px] overflow-hidden p-5">
      <h1 className="text-[#E2F1E7]">Feed</h1>
      <div className="flex p-5 flex-col gap-4 overflow-y-auto">
        {feed.results?.length === 0 && <p>No posts found</p>}
        {feed.results?.map((item, index) => (
          <PostCard key={item.id} post={item} />
        ))}
      </div>
    </div>
  );
};

export default FeedComponent;
