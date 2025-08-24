<template>
  <div
    v-show="searchActive"
    :class="{'loading': !!currentRequest}"
    class="search modern-search"
  >
    <div class="search-header">
      <span class="header-icon">🔍</span> 搜索消息
    </div>
    <div class="input-holder">
      <input
        ref="inputSearch"
        v-model.trim="search"
        class="input search-input"
        type="search"
        placeholder="输入关键词搜索消息..."
        @keydown="checkToggleSearch"
      />
      <i class="icon-cancel-circled-outline close-btn" @click="close"/>
      <div class="search-loading"/>
    </div>
    <div
      v-if="searchResultText"
      :class="['search-result', searchResult === '未找到结果' ? 'no-results' : '']"
    >
      <span class="result-icon">{{ searchResult === '未找到结果' ? '❌' : '✨' }}</span>
      {{ searchResultText }}
    </div>
  </div>
</template>
<script lang="ts">
import debounce from "lodash.debounce";
import {
  Component,
  Prop,
  Ref,
  Vue,
  Watch,
} from "vue-property-decorator";
import {RoomModel} from "@/ts/types/model";

const START_TYPING = "开始输入，消息将会出现";


let uniqueId = 1;

function getUniqueId() {
  return uniqueId++;
}

@Component({name: "SearchMessages"})
export default class SearchMessages extends Vue {
  @Prop() public room!: RoomModel;

  @Ref()
  public inputSearch!: HTMLInputElement;

  public debouncedSearch!: Function;

  public search: string = "";

  public currentRequest: number = 0;

  public searchResult: string = "";

  public get searchResultText() {
    if (this.searchResult) {
      return this.searchResult;
    } else if (this.room && this.room.search && !this.room.search.locked) {
      return "更多消息可用，滚动到顶部加载它们";
    }
    return "此搜索没有更多可用消息";
  }

  public get searchActive() {
    return this.room && this.room.search && this.room.search.searchActive;
  }

  close() {
    if (this.room) {
      this.$store.toogleSearch(this.room.id);
    }
  }

  @Watch("searchActive")
  public onSearchActiveChange(value: boolean) {
    if (value) {
      this.$nextTick(function() {
        this.inputSearch.focus();
      });
    }
  }

  public checkToggleSearch(event: KeyboardEvent) {
    if (event.key === "Escape") {
      this.$store.toogleSearch(this.room.id);
    }
  }

  public created() {
    if (this.room && this.room.search) {
      this.search = this.room.search.searchText;
    }
    if (!this.search) {
      this.searchResult = START_TYPING;
    }
    this.debouncedSearch = debounce(this.doSearch, 500);
  }

  private async doSearch(search: string) {
    if (!search || !this.room) {
      this.searchResult = START_TYPING;
      return;
    }

    const uniqueId = getUniqueId();
    try {
      this.currentRequest = uniqueId;
      await this.$messageSenderProxy.getMessageSender(this.room.id).loadUpSearchMessages(
        this.room.id,
        10,
        (found) => {
          if (found) {
            this.searchResult = "";
          } else {
            this.searchResult = "未找到结果";
          }
          if (this.currentRequest === uniqueId) {
            this.currentRequest = 0;
            return true;
          }
          return false;
        },
      );
    } catch (e: any) {
      if (uniqueId === this.currentRequest) {
        this.currentRequest = 0;
      }
      this.searchResult = e;
    }
  }

  @Watch("search")
  private onSearchChange(search: string) {
    if (this.room) {
      this.$store.setSearchTextTo({
        searchText: search,
        roomId: this.room.id,
      });
    }
    if (this.currentRequest) {
      this.currentRequest = getUniqueId();
    }
    this.debouncedSearch(search);
  }
}
</script>

<style lang="sass" scoped>
@import "@/assets/sass/partials/mixins"

.modern-search
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)
  border-radius: 15px
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1)
  padding: 25px
  margin: 15px
  backdrop-filter: blur(10px)

.search-header
  font-size: 20px
  font-weight: 600
  color: #333
  text-align: center
  margin-bottom: 20px
  padding-bottom: 15px
  border-bottom: 1px solid rgba(0, 0, 0, 0.1)

.header-icon
  font-size: 24px
  margin-right: 8px
  vertical-align: middle

.input-holder
  display: flex
  align-items: center
  background: rgba(255, 255, 255, 0.9)
  border-radius: 25px
  padding: 8px 15px
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1)
  transition: all 0.3s ease

  &:focus-within
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15)
    transform: translateY(-1px)

  .search-input
    flex-grow: 1
    border: none
    background: transparent
    font-size: 16px
    padding: 8px 10px
    outline: none
    color: #333

    &::placeholder
      color: #888

  .close-btn
    @include hover-click(#ff6b6b)
    cursor: pointer
    font-size: 20px
    margin-left: 10px
    transition: all 0.3s ease
    
    &:hover
      transform: scale(1.1)

.search
  padding: 5px

  &.loading
    .search-loading
      margin-left: 5px
      margin-bottom: -5px
      margin-top: -3px
      @include spinner(3px, #333)

.search-result
  display: flex
  align-items: center
  justify-content: center
  padding: 15px 20px
  margin-top: 15px
  border-radius: 10px
  font-size: 16px
  font-weight: 500
  transition: all 0.3s ease

  .result-icon
    margin-right: 8px
    font-size: 18px

  &.no-results
    background: rgba(255, 107, 107, 0.1)
    color: #ff6b6b
    border: 1px solid rgba(255, 107, 107, 0.3)

  &:not(.no-results)
    background: rgba(76, 175, 80, 0.1)
    color: #4caf50
    border: 1px solid rgba(76, 175, 80, 0.3)
</style>
