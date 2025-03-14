export default defineAppConfig({
    ui: {
        primary: 'blue',
        table: {
            divide: '',
            tbody: 'divide-y divide-[#323232]',
            th: {
                base: 'bg-[#323232] text-white first:w-1/6 [&:nth-child(2n)]:w-1/12 last:w-10',
            },
            tr: {
                base: 'bg-[#1b1b1d]'
            },
            td: {
                base: 'first:font-bold first:text-[#d4e8f8]'
            }
        }
    },
});
