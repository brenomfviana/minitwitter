const ProfileCard = ({ user }) => {
  return (
    <div className="rounded-md p-4 bg-[#387478]">
      <p className="text-xl font-bold">{user.name}</p>
      <p className="text-lg">@{user.username}</p>
      <p className="text-md">
        <span className="font-bold">{user.followers_count}</span> followers
      </p>
      <p className="text-md">
        <span className="font-bold">{user.following_count}</span> following
      </p>
      <p className="text-md">
        <span className="font-bold">{user.posts_count}</span> posts
      </p>
    </div>
  );
};

export default ProfileCard;
