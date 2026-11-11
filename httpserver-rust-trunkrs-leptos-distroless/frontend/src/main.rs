use leptos::prelude::*;

use shared_lib::MyStruct;

fn main() {
    mount_to_body(App);
}

#[component]
fn App() -> impl IntoView {
    let my_struct = MyStruct::new(42);

    let (count, set_count) = signal(my_struct.get_field());

    view! {
        <p>
            <div>
                <button
                    on:click=move |_| set_count.set(shared_lib::add(count.get(), 1))
                >
                    "Click to add one"
                </button>
            </div>
            <div>
                <button
                    on:click=move |_| set_count.set(shared_lib::subtract(count.get(), 1))
                >
                    "Click to remove one"
                </button>
            </div>
            <div>
                <span>Count: {count}</span>
            </div>
        </p>
    }
}
