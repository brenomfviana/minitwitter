import BaseLayout from "./layouts/BaseLayout";
import FeedComponent from "./components/FeedComponent";

function App() {
  return (
    <>
      <BaseLayout>
        <div className="flex flex-col w-full justify-center items-center gap-2">
          <h1>Mini Twitter</h1>
          <FeedComponent />
        </div>
      </BaseLayout>
    </>
  );
}

export default App;
