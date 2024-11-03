import { useState, useEffect } from "react";
import api from "../api";

const PostCard = ({ post }) => {
  const [likeCount, setLikeCount] = useState("");

  useEffect(() => {
    setLikeCount(post.like_count);
  }, []);

  const auth = JSON.parse(localStorage.getItem("auth"));
  const handleLike = (post) => {
    if (auth) {
      api.defaults.headers["Authorization"] = `Bearer ${auth.access}`;

      api
        .patch(`/posts/${post.id}/like/`)
        .then((response) => {
          setLikeCount(post.like_count + 1);
        })
        .catch((error) => {
          console.error(error);
        });
    }
  };

  return (
    <div className="rounded-md p-4 bg-[#387478]">
      <p className="font-bold">@{post.user_username}</p>
      <p>{post.text}</p>
      <div onClick={() => handleLike(post)}>Likes: {likeCount}</div>
    </div>
  );
};

export default PostCard;
