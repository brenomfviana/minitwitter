const BaseLayout = ({ children }) => {
  return (
    <>
      <main className="flex h-screen bg-[#243642]">{children}</main>
    </>
  );
};

export default BaseLayout;
