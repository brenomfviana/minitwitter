import BaseLayout from "./layouts/BaseLayout";
import FeedComponent from "./components/FeedComponent";
import ProfileComponent from "./components/ProfileComponent";

function App() {
  return (
    <>
      <BaseLayout>
        <div className="flex flex-row w-full justify-center">
          <ProfileComponent className="items-start" />
          <FeedComponent />
        </div>
      </BaseLayout>
    </>
  );
}

export default App;
