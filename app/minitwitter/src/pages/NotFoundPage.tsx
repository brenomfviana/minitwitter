import BaseLayout from "../layouts/BaseLayout";
import ButtonLink from "../components/ButtonLink";

const NotFoundPage = () => {
  return (
    <>
      <BaseLayout>
        <div className="flex w-full justify-center items-center">
          <div className="flex flex-col text-center p-10 gap-4 rounded-xl bg-[#629584]">
            <div className="flex flex-col">
              <h1 className="text-8xl">404</h1>
              <h2 className="text-md">Page Not Found</h2>
            </div>
            <ButtonLink text="Back to Login" redirect="/login" />
          </div>
        </div>
      </BaseLayout>
    </>
  );
};

export default NotFoundPage;
