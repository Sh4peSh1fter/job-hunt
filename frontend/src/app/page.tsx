import Image from "next/image";

export default function GuidePage() {
  return (
    <article className="prose lg:prose-xl dark:prose-invert max-w-none">
      <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100 sm:text-4xl">
        Welcome to Job Hunt!
      </h1>
      <p className="mt-6 text-lg leading-8 text-gray-700 dark:text-gray-300">
        This is your personal assistant to help manage and optimize your job search. 
        Navigate to the "Tools" section to explore available utilities.
      </p>
      
      <section className="mt-10">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          How to Use This Application
        </h2>
        <p className="mt-4 text-gray-700 dark:text-gray-300">
          Detailed instructions and tips will go here. For now, explore the tools and check back later for more guidance!
        </p>
        {/* Future content can be structured with more h2, p, ul, ol tags */}
      </section>

      <section className="mt-10">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          About Your Privacy
        </h2>
        <p className="mt-4 text-gray-700 dark:text-gray-300">
          All data processed by Job Hunt is stored locally on your machine. No information is sent to external servers unless you explicitly use features like Google Sheets integration (which will require your authentication).
        </p>
      </section>
    </article>
  );
}
