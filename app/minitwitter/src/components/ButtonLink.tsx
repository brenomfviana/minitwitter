import { Link } from "react-router-dom";

const ButtonLink = ({ text, redirect }) => {
  return (
    <>
      <div className="py-1 px-10 bg-[#387478] hover:bg-[#243642] text-[#E2F1E7] rounded-md">
        <Link to={redirect}>{text}</Link>
      </div>
    </>
  );
};

export default ButtonLink;
