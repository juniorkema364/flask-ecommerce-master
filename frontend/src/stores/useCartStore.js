import { create } from "zustand";
import axios from "../lib/axios";
import { toast } from "react-hot-toast";

export const useCartStore = create((set, get) => ({
	cart: [],
	coupon: null,
	total: 0,
	subtotal: 0,
	isCouponApplied: false,

	getMyCoupon: async () => {
		try {
			const response = await axios.get("/coupons");
			set({ coupon: response.data });
		} catch (error) {
			console.error("Error fetching coupon:", error);
		}
	},
	applyCoupon: async (code) => {
		try {
			const response = await axios.post("/coupons/validate", { code });
			set({ coupon: response.data, isCouponApplied: true });
			get().calculateTotals();
			toast.success("Coupon applied successfully");
		} catch (error) {
			toast.error(error.response?.data?.message || "Failed to apply coupon");
		}
	},
	removeCoupon: () => {
		set({ coupon: null, isCouponApplied: false });
		get().calculateTotals();
		toast.success("Coupon removed");
	} , 

	getCartItems: async () => {
		try {
			const res = await axios.get("/cart");
			set({ cart: res.data });
			get().calculateTotals();
		} catch (error) {
			set({ cart: [] });
			toast.error(error.response.data.message || "An error occurred");
		}
	},
	clearCart: async () => {
		set({ cart: [], coupon: null, total: 0, subtotal: 0 });
	},
	addToCart: async (product) => {
		try {
			 
			await axios.post("/cart", { product_id: product.id });
			toast.success("Produit ajouté avec succes");
	
	 
			set((prevState) => {
				 
				const existingItem = prevState.cart.find((item) => item.id === product.id);
	
				 
				const updatedCart = existingItem
					? prevState.cart.map((item) =>
							item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
					  )
					: [...prevState.cart, { ...product, quantity: 1 }];
	
				 
				return { cart: updatedCart };
			});
	
			 
			get().calculateTotals();
		} catch (error) {
			 
			toast.error(error.response?.data || "An error occurred");
			console.log(product.id)
		}
	},
	
	removeFromCart: async (product_id) => {
		try {
			 
			await axios.delete(`/cart/${product_id}`);
			toast.success('produit supprimé avec succes')
	
			 
			set((prevState) => ({
				cart: prevState.cart.filter((item) => item.id !== product_id),
			}));
	
			 
			get().calculateTotals();
		} catch (error) {
			 
			console.error("Erreur lors de la suppression du produit du panier :", error);
			toast.error("Impossible de supprimer le produit du panier. Veuillez réessayer.");
		}
	},
	updateQuantity: async (product_id, quantity) => {
		if (quantity === 0) {
			get().removeFromCart(product_id);
			return;
		}

		await axios.put(`/cart/${product_id}`, { quantity });
		set((prevState) => ({
			cart: prevState.cart.map((item) => (item.id === product_id ? { ...item, quantity } : item)),
		}));
		get().calculateTotals();
	},
	calculateTotals: () => {
		const { cart, coupon } = get();
		const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
		let total = subtotal;

		if (coupon) {
			const discount = subtotal * (coupon.discountPercentage / 100);
			total = subtotal - discount;
		}

		set({ subtotal, total });
	},
}));
