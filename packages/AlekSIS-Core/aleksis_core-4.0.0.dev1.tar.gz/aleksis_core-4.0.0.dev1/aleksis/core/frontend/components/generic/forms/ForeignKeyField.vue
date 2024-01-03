<template>
  <v-autocomplete
    v-bind="$attrs"
    v-on="$listeners"
    :items="items"
    item-value="id"
    :item-text="itemName"
    class="fc-my-auto"
  >
    <template #item="item">
      <slot name="item" v-bind="item">
        {{ item.item[itemName] }}
      </slot>
    </template>
    <template #append-outer>
      <v-btn icon @click="menu = true">
        <v-icon>$plus</v-icon>
      </v-btn>

      <slot
        name="createComponent"
        :attrs="{
          value: menu,
          defaultItem: defaultItem,
          gqlQuery: gqlQuery,
          gqlCreateMutation: gqlCreateMutation,
          gqlPatchMutation: gqlPatchMutation,
          isCreate: true,
          fields: fields,
          getCreateData: getCreateData,
          createItemI18nKey: createItemI18nKey,
        }"
        :on="{
          input: (i) => (menu = i),
          cancel: () => (menu = false),
          save: handleSave,
          update: handleUpdate,
        }"
      >
        <dialog-object-form
          v-model="menu"
          @cancel="menu = false"
          @update="handleUpdate"
          @save="handleSave"
          @error="handleError"
          :is-create="true"
          :default-item="defaultItem"
          :fields="fields"
          :gql-query="gqlQuery"
          :gql-patch-mutation="gqlPatchMutation"
          :gql-create-mutation="gqlCreateMutation"
          :create-item-i18n-key="createItemI18nKey"
          :get-create-data="getCreateData"
        >
          <template
            v-for="(_, name) in $scopedSlots"
            :slot="name"
            slot-scope="slotData"
          >
            <slot :name="name" v-bind="slotData" />
          </template>
        </dialog-object-form>
      </slot>

      <closable-snackbar :color="snackbarState" v-model="snackbar">
        {{ snackbarText }}
      </closable-snackbar>
    </template>
  </v-autocomplete>
</template>

<script>
import ClosableSnackbar from "../dialogs/ClosableSnackbar.vue";
import DialogObjectForm from "../dialogs/DialogObjectForm.vue";

export default {
  name: "ForeignKeyField",
  components: { ClosableSnackbar, DialogObjectForm },
  extends: "v-autocomplete",
  data() {
    return {
      menu: false,
      snackbar: false,
      snackbarState: "error",
      snackbarText: "",
    };
  },
  apollo: {
    items() {
      return {
        query: this.gqlQuery,
      };
    },
  },
  methods: {
    handleUpdate(store, createdObject) {
      // Read the data from cache for query
      const storedData = store.readQuery({ query: this.gqlQuery });

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const storedDataKey = Object.keys(storedData)[0];

      // Add item to stored data
      storedData[storedDataKey].push(createdObject);

      // Write data back to the cache
      store.writeQuery({ query: this.gqlQuery, data: storedData });
    },
    handleSave(data) {
      let newItem =
        data.data[this.gqlCreateMutation.definitions[0].name.value].item;
      let newValue = "return-object" in this.$attrs ? newItem : newItem.id;
      let modelValue =
        "multiple" in this.$attrs
          ? Array.isArray(this.$attrs.value)
            ? this.$attrs.value.concat(newValue)
            : [newValue]
          : newValue;

      this.$emit("input", modelValue);
    },
    slotName(field) {
      return field.value + ".field";
    },
    handleError(error) {
      console.error(error);
      if (error instanceof String) {
        // error is a translation key or simply a string
        this.snackbarText = this.$t(error);
      } else if (error instanceof Object && error.message) {
        this.snackbarText = error.message;
      } else {
        this.snackbarText = this.$t("graphql.snackbar_error_message");
      }
      this.snackbarState = "error";
      this.snackbar = true;
    },
  },
  props: {
    defaultItem: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    gqlQuery: {
      type: Object,
      required: true,
    },
    gqlCreateMutation: {
      type: Object,
      required: true,
    },
    gqlPatchMutation: {
      type: Object,
      required: true,
    },
    getCreateData: {
      type: Function,
      required: false,
      default: (item) => item,
    },
    itemName: {
      type: [String, Function],
      required: false,
      default: "name",
    },
    createItemI18nKey: {
      type: String,
      required: false,
      default: "actions.create",
    },
  },
};
</script>

<style scoped>
.fc-my-auto > :first-child {
  margin-block: auto;
}
</style>
