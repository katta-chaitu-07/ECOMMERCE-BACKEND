
import streamlit as st

from services.order import get_orders, get_order_by_id


def render_orders_page():

    st.title("📦 My Orders")
    st.caption("Track your purchases and view order details.")

    # Check authentication
    if not st.session_state.get("access_token") and not st.session_state.get("token"):
        st.warning("Please log in to view your orders.")

        if st.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()

        return

    # Load order history
    with st.spinner("Loading your orders..."):
        result = get_orders()

    if not result["success"]:
        st.error(result["error"])
        return

    orders = result["data"]

    # Handle empty order history
    if not orders:
        st.info("You haven't placed any orders yet.")

        if st.button("Start Shopping"):
            st.session_state.page = "Products"
            st.rerun()

        return

    st.subheader(f"Your Order History ({len(orders)})")

    # Display each order
    for order in orders:

        order_id = order["order_id"]
        total = order["total_amount"]
        order_status = order["status"]
        created_at = order.get("created_at")

        with st.container(border=True):

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f"**Order #{order_id}**")
                st.caption(created_at or "Date unavailable")

            with col2:
                st.write(f"Total: ₹{total:,.2f}")
                st.write(f"Status: {order_status.title()}")

            with col3:
                if st.button(
                    "View Details",
                    key=f"view_order_{order_id}",
                    use_container_width=True
                ):
                    st.session_state.selected_order_id = order_id
                    st.rerun()

    # Display selected order details
    selected_order_id = st.session_state.get("selected_order_id")

    if selected_order_id:

        st.divider()
        st.subheader(f"Order Details #{selected_order_id}")

        with st.spinner("Loading order details..."):
            detail_result = get_order_by_id(selected_order_id)

        if detail_result["success"]:

            order = detail_result["data"]

            st.write(f"**Status:** {order['status'].title()}")
            st.write(
                f"**Total Amount:** ₹{order['total_amount']:,.2f}"
            )

            st.markdown("### Purchased Products")

            for item in order.get("items", []):

                with st.container(border=True):

                    st.markdown(f"**{item['product_name']}**")
                    st.write(f"Quantity: {item['quantity']}")
                    st.write(
                        f"Unit Price: ₹{item['unit_price']:,.2f}"
                    )
                    st.write(
                        f"Subtotal: ₹{item['subtotal']:,.2f}"
                    )

        else:
            st.error(detail_result["error"])

        if st.button("Close Order Details"):
            del st.session_state.selected_order_id
            st.rerun()

    st.divider()

    if st.button("← Continue Shopping"):
        st.session_state.page = "Products"
        st.rerun()
