import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

GITHUB_REPO = "https://github.com/arcsikex/magyar_film_maraton"
YOUTUBE = "https://www.youtube.com"
primary_color = tc = st.get_option("theme.primaryColor").replace("#", "")

data: pd.DataFrame = pd.read_csv("mafima.csv", delimiter=";")


def main():
    st.set_page_config(
        page_title="Magyar Film Maraton",
        page_icon="🍿",
    )
    with st.sidebar:
        st.subheader("Szűrők")
        year_filter = st.slider(
            "Bemutatás éve",
            int(data["Év"].min()),
            int(data["Év"].max()),
            (int(data["Év"].min()), int(data["Év"].max())),
        )
        filtered_data: pd.DataFrame = data[
            (data["Év"] >= year_filter[0]) & (data["Év"] <= year_filter[1])
        ]

        length = st.slider(
            "Játékidő [perc]",
            int(data["Játékidő [perc]"].min()),
            int(data["Játékidő [perc]"].max()),
            (
                int(data["Játékidő [perc]"].min()),
                int(data["Játékidő [perc]"].max()),
            ),
        )
        filtered_data: pd.DataFrame = filtered_data[
            (filtered_data["Játékidő [perc]"] >= length[0])
            & (filtered_data["Játékidő [perc]"] <= length[1])
        ]

        rating = st.slider("Értékelés", -1, 10, (-1, 10))
        filtered_data = filtered_data[
            (filtered_data["Értékelés"] >= rating[0])
            & (filtered_data["Értékelés"] <= rating[1])
        ]

        st.divider()
        st.markdown(
            f"Socials: \
            [![Github](https://img.icons8.com/?size=40&id=fmFqQmR0UdsR&format=png&color={primary_color})]({GITHUB_REPO}) | \
            [![YouTube](https://img.icons8.com/?size=40&id=NgVx6SS0Wbjb&format=png&color={primary_color})]({YOUTUBE})"
        )

    filtered_data = filtered_data.sort_values("Értékelés", ascending=False)

    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Magyar Film Maraton Toplista</h1>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Ez az oldal a Magyar Film Maraton sorozatban bemutatott filmeket foglalja össze egy táblázatban, ahol a Review oszlopban található linkekkel érheted el az egyes filmek értékelését. Az alábbi lejátszási listában megtalálod a sorozat összes epizódját, az oldalsávban pedig szűrők segítik a keresést.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; background: #000; max-width: 1280px; max-height: 720px; margin: auto;">
        <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
                src="https://www.youtube.com/embed/videoseries?si=hY9MZAi0jL3n4Je_&amp;list=PLAuHYXdwFUwg8ErChl6ZtdloiZg4xI55K"
                title="Magyar Film Maraton"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen>
        </iframe>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()

    # Configure AgGrid options
    gb = GridOptionsBuilder.from_dataframe(filtered_data)
    gb.configure_column("Link", type=["htmlCell"])
    gb.configure_column("Borítókép", type=["htmlCell"])

    gb.configure_column(
        "Borítókép",
        headerName="Borítókép",
        cellRenderer=JsCode(
            """
        class ImageCellRenderer {
          init(params) {
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `<div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
                                      <img src='${params.value}' style='max-height: 100px; width: auto; height: auto;' />
                                   </div>`;
          }
          getGui() {
            return this.eGui;
          }
        }
    """
        ),
    )

    gb.configure_column(
        "Link",
        headerName="Review",
        cellRenderer=JsCode(
            """
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Link';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """
        ),
    )

    gb.configure_grid_options(rowHeight=100)
    grid_options = gb.build()

    # Display the data with AgGrid
    AgGrid(
        filtered_data,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        theme="streamlit",
        fit_columns_on_grid_load=True,
        height=len(filtered_data.index) * 100 + 35,
    )
    st.text("*-1: Nem kapott értékelést (A film nem volt megtalálható)")
    st.divider()
    st.markdown(
        """
        ### Források a táblázathoz:
        - Lista és értékelés a [Magyar Film Maraton](https://www.youtube.com/playlist?list=PLAuHYXdwFUwg8ErChl6ZtdloiZg4xI55K) lejátszási listáról.
        - Hossz és bemutatás éve: [port.hu](https://port.hu/)
        - Borítóképek: [IMDB](https://www.imdb.com/), [port.hu](https://port.hu/)
        """
    )


if __name__ == "__main__":
    main()
